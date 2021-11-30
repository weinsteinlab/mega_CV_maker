#!/bin/bash

cp ~/bashrc_copy ~/.bashrc
source ~/.bashrc
conda create -n md_analysis -y python=3.6
conda activate md_analysis
conda install -y -c conda-forge mdanalysis
