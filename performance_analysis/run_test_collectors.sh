#!/bin/bash

collector_keys="collector_keys.csv"
pid_file="simulator_pids.txt"
exec 3< "$collector_keys"

> "$pid_file"

for _ in $(seq 1 "$1"); do
  IFS=, read -r key lat long aeroporto <&3

  if [ -z "$key" ]; then
    echo "Fim do arquivo alcançado ou linha inválida."
    break
  fi

  python3 simulator_manager.py "$key" "$lat" "$long" "$aeroporto" &
  echo $! >> "$pid_file"
#  sleep 90
done

exec 3<&-
