#!/bin/bash

# Define two arrays
BitsPC=(16 20)
globalH=(2 6 8 16 20)

# Iterate over the elements of the first array
for bit in "${BitsPC[@]}"; do
    # Iterate over the elements of the second array
    for hist in "${globalH[@]}"; do
        start=$(date +%s.%N)
        python3 branch_predictor.py --bp 3 -n "$bit" -g "$hist" | grep "% predicciones correctas:">> output.txt
        end=$(date +%s.%N)
        execution_time=$(echo "$end - $start" | bc)
        echo "PCbits: $bit , global hist: $hist Execution time: $execution_time seconds">> output.txt
        echo "--">> output.txt
    done
done
