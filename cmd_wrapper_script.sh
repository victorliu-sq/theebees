# turn on bash's job control
set -m

# Start the cpudist kprobe
python3 ./cpudist.py -P -e 1 &

# Start the counter process
python3 ./counter.py

# now we bring the primary process back into the foreground
# and leave it there
fg %1