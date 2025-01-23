#!/bin/bash

collector_keys="collector_keys.csv"

exec 3< "$collector_keys"

for _ in $(seq 1 "$1"); do
  IFS=, read -r key lat long aeroporto <&3

  if [ -z "$key" ]; then
    echo "Fim do arquivo alcançado ou linha inválida."
    break
  fi

  python3 simulator_manager.py "$key" "$lat" "$long" "$aeroporto" &
  echo "Collector $key was started with success" >> collectors_started_list.txt
  sleep 180
done

exec 3<&-

echo "Processamento concluído."