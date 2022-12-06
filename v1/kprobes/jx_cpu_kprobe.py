#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports
#
# cpudist   Summarize on- and off-CPU time per task as a histogram.
#
# USAGE: cpudist [-h] [-O] [-T] [-m] [-P] [-L] [-p PID] [-I] [-e] [interval] [count]
#
# This measures the time a task spends on or off the CPU, and shows this time
# as a histogram, optionally per-process.
#
# By default CPU idle time are excluded by simply excluding PID 0.
#
# Copyright 2016 Sasha Goldshtein
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 27-Mar-2022   Rocky Xing      Changed to exclude CPU idle time by default.
# 25-Jul-2022   Rocky Xing      Added extension summary support.

from __future__ import print_function
from bcc import BPF
from time import sleep, strftime
import argparse
import math
import ctypes
import json
from collections import defaultdict
import sys

examples = """examples:
    cpudist              # summarize on-CPU time as a histogram
    cpudist -O           # summarize off-CPU time as a histogram
    cpudist 1 10         # print 1 second summaries, 10 times
    cpudist -mT 1        # 1s summaries, milliseconds, and timestamps
    cpudist -P           # show each PID separately
    cpudist -p 185       # trace PID 185 only
    cpudist -I           # include CPU idle time
    cpudist -e           # show extension summary (average/total/count)
"""
parser = argparse.ArgumentParser(
    description="Summarize on- and off-CPU time per task as a histogram.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
# long notation --: name of argument
# short notation -: help flag
# action="store_true", default is false, this variable becomes true if given a value
parser.add_argument("-O", "--offcpu", action="store_true",
    help="measure off-CPU time")
parser.add_argument("-T", "--timestamp", action="store_true",
    help="include timestamp on output")
parser.add_argument("-m", "--milliseconds", action="store_true",
    help="millisecond histogram")
parser.add_argument("-P", "--pids", action="store_true",
    help="print a histogram per process ID")
parser.add_argument("-L", "--tids", action="store_true",
    help="print a histogram per thread ID")
parser.add_argument("-p", "--pid",
    help="trace this PID only")
parser.add_argument("-I", "--include-idle", action="store_true",
    help="include CPU idle time")
parser.add_argument("-e", "--extension", action="store_true",
    help="show extension summary (average/total/count)")
parser.add_argument("interval", nargs="?", default=99999999,
    help="output interval, in seconds")
parser.add_argument("count", nargs="?", default=99999999,
    help="number of outputs")
parser.add_argument("--ebpf", action="store_true",
    help=argparse.SUPPRESS)


parser.add_argument("-d", "--database", 
    help="path of database")

args = parser.parse_args()

debug = 0

# countdown = int(args.count)
# countdown = 5

# ********************************************************************
args.extension = 1
args.pid = 3327
args.interval = 1

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
"""

if not args.offcpu:
    bpf_text += "#define ONCPU\n"

bpf_text += """
typedef struct entry_key {
    u32 pid;
    u32 cpu;
} entry_key_t;

typedef struct pid_key {
    u64 id;
    u64 slot;
} pid_key_t;

typedef struct ext_val {
    u64 total;
    u64 count;
    u64 max;
} ext_val_t;

BPF_HASH(start, entry_key_t, u64, MAX_PID);
STORAGE

static inline void store_start(u32 tgid, u32 pid, u32 cpu, u64 ts)
{
    if (PID_FILTER)
        return;

    if (IDLE_FILTER)
        return;

    entry_key_t entry_key = { .pid = pid, .cpu = cpu };
    start.update(&entry_key, &ts);
}

static inline void update_hist(u32 tgid, u32 pid, u32 cpu, u64 ts)
{
    if (PID_FILTER)
        return;

    if (IDLE_FILTER)
        return;

    entry_key_t entry_key = { .pid = pid, .cpu = cpu };
    u64 *tsp = start.lookup(&entry_key);
    if (tsp == 0)
        return;

    if (ts < *tsp) {
        // Probably a clock issue where the recorded on-CPU event had a
        // timestamp later than the recorded off-CPU event, or vice versa.
        return;
    }
    u64 delta = ts - *tsp;
    FACTOR
    STORE
}

int sched_switch(struct pt_regs *ctx, struct task_struct *prev)
{
    u64 ts = bpf_ktime_get_ns();
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 tgid = pid_tgid >> 32, pid = pid_tgid;
    u32 cpu = bpf_get_smp_processor_id();

    u32 prev_pid = prev->pid;
    u32 prev_tgid = prev->tgid;
#ifdef ONCPU
    update_hist(prev_tgid, prev_pid, cpu, ts);
#else
    store_start(prev_tgid, prev_pid, cpu, ts);
#endif

BAIL:
#ifdef ONCPU
    store_start(tgid, pid, cpu, ts);
#else
    update_hist(tgid, pid, cpu, ts);
#endif

    return 0;
}
"""

if args.pid:
    bpf_text = bpf_text.replace('PID_FILTER', 'tgid != %s' % args.pid)
else:
    bpf_text = bpf_text.replace('PID_FILTER', '0')

# set idle filter
idle_filter = 'pid == 0'
if args.include_idle:
    idle_filter = '0'
bpf_text = bpf_text.replace('IDLE_FILTER', idle_filter)

if args.milliseconds:
    bpf_text = bpf_text.replace('FACTOR', 'delta /= 1000000;')
    label = "msecs"
else:
    bpf_text = bpf_text.replace('FACTOR', 'delta /= 1000;')
    label = "usecs"

storage_str = ""
store_str = ""

if args.pids or args.tids:
    section = "pid"
    pid = "tgid"
    if args.tids:
        pid = "pid"
        section = "tid"
    storage_str += "BPF_HISTOGRAM(dist, pid_key_t, MAX_PID);"
    store_str += """
    pid_key_t key = {.id = """ + pid + """, .slot = bpf_log2l(delta)};
    dist.increment(key);
    """
else:
    section = ""
    storage_str += "BPF_HISTOGRAM(dist);"
    store_str += "dist.atomic_increment(bpf_log2l(delta));"

if args.extension:
    storage_str += "BPF_ARRAY(extension, ext_val_t, 1);"
    store_str += """
    u32 index = 0;
    ext_val_t *ext_val = extension.lookup(&index);
    if (ext_val) {
        lock_xadd(&ext_val->total, delta);
        lock_xadd(&ext_val->count, 1);
        // GET THE MAX USECS
        if (delta > ext_val->max) {
            lock_xadd(&ext_val->max, delta - ext_val->max);
            // ext_val->max = delta;
        }
    }
    """

bpf_text = bpf_text.replace("STORAGE", storage_str)
bpf_text = bpf_text.replace("STORE", store_str)

if debug or args.ebpf:
    print(bpf_text)
    
    if args.ebpf:
        exit()

max_pid = int(open("/proc/sys/kernel/pid_max").read())

b = BPF(text=bpf_text, cflags=["-DMAX_PID=%d" % max_pid])
b.attach_kprobe(event_re="^finish_task_switch$|^finish_task_switch\.isra\.\d$",
                fn_name="sched_switch")

print("Tracing %s-CPU time... Hit Ctrl-C to end." %
      ("off" if args.offcpu else "on"))

exiting = 0 if args.interval else 1
dist = b.get_table("dist")
if args.extension:
    extension = b.get_table("extension")

# buckets for oncpu metrics
bucket_idx2count = defaultdict(int)
# range : count

# Initialization
# current_metrics_cpu
cur_metrics_cpu = {}
# time
curTime = 0
# max_use_cs
max_bucket_num = 0

# initialize cpu.json: cpu, avg_cpu, sum_cpu
data = {}

# print(args.database)
db_path = args.database
# with open('%s.json' % args.database, "w") as f:
import sys
with open(db_path, "w") as f:
    data["cpu_avg"] = defaultdict(float)
    data["cpu_sum"] = defaultdict(int)
    data["cpu"] = []
    json.dump(data, f)
# Record interval
RECORD_TIME_INTERVAL = 5

while (1):
    curTime += 1
    print("Current Time is:", curTime)
    if (curTime+1) % 5 != 0:
        continue
    try:
        sleep(int(args.interval))
    except KeyboardInterrupt:
        exiting = 1

    if args.timestamp:
        print("%-8s\n" % strftime("%H:%M:%S"), end="")

    def pid_to_comm(pid):
        try:
            comm = open("/proc/%d/comm" % pid, "r").read()
            return "%d %s" % (pid, comm)
        except IOError:
            return str(pid)
    dist.print_log2_hist(label, section, section_print_fn=pid_to_comm)

    # update max usecs
    cur_max_usecs = 0
    if args.extension:
        total = extension[0].total
        count = extension[0].count
        cur_max_usecs = extension[0].max
        # update max_usecs

        if count > 0:
            print("\navg = %ld %s, total: %ld %s, count: %ld, max: %ld\n" %
                (total / count, label, total, label, count, cur_max_usecs))
        # Clear the extension
        extension.clear()

    # Get the number of buckets
    if cur_max_usecs == 0:
        cur_max_usecs += 1
    n = int(math.log2(cur_max_usecs)) + 1
    # update max bucket num
    if n > max_bucket_num:
        max_bucket_num = n
    print("num of buckets is %ld" % n)
    print("max num of buckets is %ld" % max_bucket_num)
    # create the histogram in user space
    # store items in dist in the newly created histogram
    data = {}
    metrics_cpu = []
    metrics_cpu_sum = defaultdict(int)
    metrics_cpu_avg = defaultdict(float)
    print("Read CPU metrics from a json File")
    with open(db_path, "r") as f:
        data = json.load(f)
        # print(data["cpu"])
        metrics_cpu_sum = data["cpu_sum"]
        metrics_cpu_avg = data["cpu_avg"]
        metrics_cpu = data["cpu"]
        # print(metrics_cpu)

    # Update cpu metrics with current cur_cpu_metrics
    for k, v in dist.items():
        # k is index of bucket(1-index) and v is count
        # print(k, v)
        k, v = k.value, v.value
        if k == 0 or k - 1 >= n:
            continue
        l, h = 1 << (k - 1), (1 << k) - 1
        if k == 1:
            l = 0
        bucket_range = str(l) + "-" + str(h)
        # print(bucket_range)
        i = k - 1
        bucket_idx2count[i] = max(v, bucket_idx2count[i])
        # update the 3 metrics
        cur_metrics_cpu[bucket_range] = bucket_idx2count[i]
        print(bucket_range, bucket_idx2count[i])
        if bucket_range in metrics_cpu_sum:
            metrics_cpu_sum[bucket_range] += bucket_idx2count[i]
        else:
            metrics_cpu_sum[bucket_range] = bucket_idx2count[i]
        metrics_cpu_avg[bucket_range] = metrics_cpu_sum[bucket_range] / ((curTime + 1) // RECORD_TIME_INTERVAL)

    time_range = curTime + 1
    # time_range = str(curTime + 1 - RECORD_TIME_INTERVAL) + "-" + str(curTime)
    cur_metrics_cpu["time-range"] = time_range 
    metrics_cpu += [cur_metrics_cpu]
    data["cpu_sum"] = metrics_cpu_sum
    data["cpu_avg"] = metrics_cpu_avg
    # data["cpu"] = metrics_cpu

    # print("=================================================================")
    # print("current CPU:", cur_metrics_cpu)
    print("=================================================================")
    print("CPU_sum:", metrics_cpu_sum)
    print("=================================================================")
    print("CPU_avg:", metrics_cpu_avg)
    print("=================================================================")
    # print("current json file", metrics_cpu)
    # print("=================================================================")

    # Write udpate metrics back into the file
    print("Write CPU metrics into a json File")
    with open(db_path, "w") as f:
        json.dump(data, f)

    dist.clear()
    cur_metrics_cpu = {}

    if exiting:
        exit()

    
