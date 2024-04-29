#!/bin/bash

# Define two arrays
BitsPC=(4 8 12 16 20)
globalH=(2 6 8 16 20)

# Iterate over the elements of the first array
for bit in "${BitsPC[@]}"; do
    # Iterate over the elements of the second array
    for hist in "${globalH[@]}"; do
        # Execute the Python script with arguments
        python3 branch_predictor.py -n "$bit" -g "$hist"
    done
done
