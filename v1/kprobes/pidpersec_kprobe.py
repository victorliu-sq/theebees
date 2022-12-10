#!/usr/bin/env python
# @lint-avoid-python-3-compatibility-imports
#
# pidpersec Count new processes (via fork).
#           For Linux, uses BCC, eBPF. See .c file.
#
# USAGE: pidpersec
#
# Written as a basic example of counting an event.
#
# Copyright (c) 2015 Brendan Gregg.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 11-Aug-2015   Brendan Gregg   Created this.

from bcc import BPF
from ctypes import c_int
from time import sleep, strftime
import argparse
import sys
import json
from collections import defaultdict
# arguments
parser = argparse.ArgumentParser(
    description="Summarize on- and off-CPU time per task as a histogram.",
    formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-d", "--database", 
    help="path of database")

args = parser.parse_args()
 
db_path = args.database
# print(db_path)

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
enum stat_types {
    S_COUNT = 1,
    S_MAXSTAT
};
BPF_ARRAY(stats, u64, S_MAXSTAT);
static void stats_increment(int key) {
    stats.atomic_increment(key);
}
void do_count(struct pt_regs *ctx) { stats_increment(S_COUNT); }
""")
b.attach_kprobe(event="sched_fork", fn_name="do_count")

# stat indexes
S_COUNT = c_int(1)

# header
print("Tracing... Ctrl-C to end.")


total_time = 0
# output
while (1):
    try:
        sleep(1)
    except KeyboardInterrupt:
        exit()

    # print("%s: PIDs/sec: %d" % (strftime("%H:%M:%S"),
    #     b["stats"][S_COUNT].value))
    
    data = {}
    value_sum = 0
    print("Read pidpersec from json file")
    with open(db_path, "r") as f:
        data = json.load(f)
        value_sum = data["pidpersec_sum"]
    
    total_time += 1
    value_sum += b["stats"][S_COUNT].value
    value_avg = float(value_sum) / float(total_time)
    
    print("Write pidpersec into json file")
    with open(db_path, "w") as f:
        data["pidpersec_avg"] = value_avg
        data["pidpersec_sum"] = value_sum
        print("%s: SUM_PIDs/sec: %d, AVG_PIDs/sec: %f" % (strftime("%H:%M:%S"),data["pidpersec_sum"],data["pidpersec_avg"]))
        json.dump(data, f)
    
    b["stats"].clear()