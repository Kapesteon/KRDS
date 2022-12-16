#!/bin/bash

apt-get install net-tools

nstat=$(netstat -an | grep "ESTABLISHED" | grep "6900")

isloged="0"

while true
do
    if [ "$nstat" != "" ] && [ "$isloged" == "0" ]
    then
        isloged="1"
        python3 /dbClient/connect.py
    fi
    if [ "$nstat" == "" ] || [ "$isloged" == "1" ]
    then
        isloged="0"
        python3 /dbClient/disconnect.py
    fi
    sleep 300
done
