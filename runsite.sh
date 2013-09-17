#!/bin/sh

flappserver restart `pwd`/flapp
sleep 2
cmd="/home/arc/LeastAuthority_env/bin/python -u `pwd`/lae_site/main.py"
pids=$(pgrep -fl "$cmd" |cut -f1 -d' ')
if [ "$pids" != "" ]; then
       echo killing $pids
       kill $pids
fi
sleep .1
PYTHONPATH=. authbind --deep sh -c "$cmd"' "$@" >>../site.out 2>&1' &
sleep .1
pgrep -fl "$cmd"
