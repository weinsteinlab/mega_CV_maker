#!/bin/bash

num_pairs=2563980
stride=26164

for i in $(seq 0 $stride $num_pairs); do
	echo $i
	sbatch submit.sh $i $((i+stride))
done

