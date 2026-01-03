#!/bin/bash
# Step 2: Reuse FL results from k=1-7

source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch

cd /home/kimnal0/auto-code-rover/hotswap
python reuse_fl_results.py
