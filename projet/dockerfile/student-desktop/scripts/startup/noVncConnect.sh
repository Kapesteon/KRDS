#!/bin/bash

python3 /dbClient/connect.py



while true
do
    python3 /dbClient/disconnect.py
    sleep 60
done
