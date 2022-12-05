# bcc

BPF_HASH / BPF_ARRAY / BPF_TABLE ARE data structures exported by the kernel,

BPF_HASH and BPF_ARRAY are simply wrappers around BPF_TABLE, which is the most basic map



## BPF_HASH

Syntax: `BPF_HASH(name [, key_type [, leaf_type [, size]]])`

Defaults: `BPF_HASH(name, key_type=u64, leaf_type=u64, size=10240)`

Ex:

```C
BPF_HASH(start, struct request *);
```

This creates a hash named `start` where the key is a `struct request *`, and the value defaults to u64.



In this program

"start" is a hashmap {entry_key, timestamp}



## BPF_HISTOGRAM

Syntax: `BPF_HISTOGRAM(name [, key_type [, size ]])`

Defaults: `BPF_HISTOGRAM(name, key_type=int, size=64)`



In this program,

"disgram" is bpf_histogram with key:[pid + slot]



## BPF_ARRAY

Syntax: `BPF_ARRAY(name [, leaf_type [, size]])`

Creates an int-indexed array which is optimized for fastest lookup and update, named `name`, with optional parameters.

Defaults: `BPF_ARRAY(name, leaf_type=u64, size=10240)`



In this program,

"extension" is bpf_array of length 1 with value:[ext_val_t]



## ts/tgid/pid/cpu

u64 ts: time stamp

Syntax: `u64 bpf_ktime_get_ns(void)`

Return: u64 number of nanoseconds. Starts at system boot time but stops during suspend.



u32 tgid: thread group id 



u32 pid: process id



u32 cpu: cpu_id



## Function

### bpf_log2l()

Syntax: `unsigned int bpf_log2l(unsigned long v)`

Returns the log-2 of the provided value. This is often used to create indexes for histograms, to construct power-of-2 histograms.



### print_log2_hist()

Syntax: `table.print_log2_hist(val_type="value", section_header="Bucket ptr", section_print_fn=None)`

Prints a table as a log2 histogram in ASCII. The table must be stored as log2, which can be done using the BPF function `bpf_log2l()`.



# Code(C + Python)

## Replace

if 0, return = ignore



PID_FILTER:

(1) if args.pid is true: if tgid != args.pid, return / if tgid == args.pid, store_start

(2) if args.pid is false: ignore



IDLE_FILTER

(1) if args.include_idle == true: if pid == 0, return

(2) if args.include_idle == false: ignore



FACTOR

delta of timestamps /= 1000 or 1000000



STORAGE

initialize (1) histogram (2) array of len 1 to store total & count



STORE

(1) histogram



(2) extension

```c
once we call STORAGE
if extension
	total += delta
    count += 1
```



BAIL



## bcc

## initialize BPF with max_pid

Syntax: `BPF({text=BPF_program | src_file=filename} [, usdt_contexts=[USDT_object, ...]] [, cflags=[arg1, ...]] [, debug=int])`

Creates a BPF object. This is the main object for defining a BPF program, and interacting with its output.



(1) Exactly one of `text` or `src_file` must be supplied (not both).

(2) The `cflags` specifies additional arguments to be passed to the compiler

```python
max_pid = int(open("/proc/sys/kernel/pid_max").read())

b = BPF(text=bpf_text, cflags=["-DMAX_PID=%d" % max_pid])
```



## attach kprobe

Syntax: `BPF.attach_kprobe(event="event", fn_name="name")`

Instruments the kernel function `event()` using kernel dynamic tracing of the function entry, and attaches our C defined function `name()` to be called when the kernel function is called.

```python
b.attach_kprobe(event_re="^finish_task_switch$|^finish_task_switch\.isra\.\d$",
                fn_name="sched_switch")
```



# Runnable Code

```shell
# python3
sudo python3 ./cpudist.py -p 1180882 -e 1

sudo python3 ./cpu_dist/jx_cpu_kprobe.py -p 3327 -e 1

# check all processes
sudo python3 ./cpu_dist/test_cpu_kprobe.py -P -e 1
```

