#!/bin/sh

netstat -nlpte | grep "rqlite" | awk '{sub(/\/.*/, "", $NF); print $NF}' | xargs -i kill -kill {}