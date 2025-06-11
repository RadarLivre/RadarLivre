#!/bin/bash

pid_file="web_clients_pids.txt"

> "$pid_file"

for i in $(seq 1 "$1"); do
    python3 web_client_simulator.py "$i" &
    echo $! >> "$pid_file"

    sleep 15
done
