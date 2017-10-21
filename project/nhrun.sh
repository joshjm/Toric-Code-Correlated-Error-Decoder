#!/bin/bash
rm nohup.out
/bin/date
nohup nice -n 10 ~/honours/nohupscript.sh &
exit 0
