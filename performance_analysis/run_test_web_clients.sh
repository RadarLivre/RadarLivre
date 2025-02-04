#!/bin/bash

CLIENT_COUNT=${1:-1}
pid_file="web_clients_pids.txt"

> "$PID_FILE"

for i in $(seq 1 "$1"); do
    python3 web_client_simulator.py "client_$i" &
    echo $! >> "$PID_FILE"

    sleep 15
done

echo "$CLIENT_COUNT clientes iniciados. PIDs salvos em $PID_FILE"