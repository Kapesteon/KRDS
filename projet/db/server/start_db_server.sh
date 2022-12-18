#!/bin/sh

rqliteDir='rqlite-v7.13.0-linux-amd64'

["$1" == ""] && ip='localhost' || ip=$1

echo $ip


# Node id
id0='rqlite-0'
id1='rqlite-1'
id2='rqlite-2'

# API Request Listening Port 
rp0='4001'
rp1='4003'
rp2='4005'

# Cluster Listening port
cp0='4002'
cp1='4004'
cp2='4006'

start_node0="./$rqliteDir/rqlited -node-id=$id0 -http-addr=$ip:$rp0 -raft-addr=$ip:$cp0 ~/node"
start_node1="./$rqliteDir/rqlited -node-id=$id1 -http-addr=$ip:$rp1 -raft-addr=$ip:$cp1 -join http://$ip:$rp0 ~/node"
start_node2="./$rqliteDir/rqlited -node-id=$id2 -http-addr=$ip:$rp2 -raft-addr=$ip:$cp2 -join http://$ip:$rp0  ~/node"

$start_node0 &
sleep 2
$start_node1 & 
sleep 2
$start_node2 & 

jobs
sleep 1
python3 initDatabase.py $ip $rp0
