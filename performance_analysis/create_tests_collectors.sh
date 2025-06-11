#!/bin/bash

cd ..

collectors_info="performance_analysis/test_collectors_infos.csv"
collector_keys="performance_analysis/collector_keys.csv"

while IFS=, read -r user lat long aeroporto local; do
  output=$(python3 manage.py createcollector $user $lat $long | awk '{print $4}')
  echo "$output,$lat,$long,$aeroporto" >> "$collector_keys"
done < "$collectors_info"

echo "All collectors were created with success!"