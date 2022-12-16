#!/bin/sh

rqliteDir='rqlite-v7.13.0-linux-amd64'
ip=$1

# Node id
id0='rqlite-0'
id1='rqlite-1'
id2='rqlite-2'

# API Request Listening Port 
rlp0='4001'
rlp1='4003'
rlp2='4005'

# Cluster Listening port
clp0='4002'
clp1='4004'
clp2='4006'

start_node1="$rqliteDir/rqlited -node-id=$id0 -http-addr=$ip:$rlp0 -raft-addr=$ip:$clp0 0"
start_node2="$rqliteDir/rqlited -node-id=$id1 -http-addr=$ip:$rlp1 -raft-addr=$ip:$clp1 1"
start_node3="$rqliteDir/rqlited -node-id=$id2 -http-addr=$ip:$rlp2 -raft-addr=$ip:$clp2 2"

./$start_node1 & ./$start_node2 & $start_node3 & python initdataBase.py