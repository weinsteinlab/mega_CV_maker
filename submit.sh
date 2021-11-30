#!/bin/bash
#SBATCH -A BIP109
#SBATCH -J test
#SBATCH -N 1
#SBATCH -t 2:00:00

cp ~/bashrc_copy ~/.bashrc
source ~/.bashrc
conda activate md_analysis2
which python3

python3 -u python_scripts/check.py
#python3 -u python_scripts/step1.py
#python3 -u python_scripts/pairs_num.py 
#python3 python_scripts/make_CVs.py $1 $2
#python python_scripts/multi_algorithm.py $1 $2

#####ask if curious about the alternate algorithms####
#python python_scripts/struct_matched_algorithm.py $1 $2
#python python_scripts/algorithm.py $1 $2
#python -u python_scripts/post_process.py
