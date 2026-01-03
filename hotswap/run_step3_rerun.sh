#!/bin/bash
# Step 3: Re-run ACR for k=8 (5 repetitions)

source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch

cd /home/kimnal0/auto-code-rover/hotswap
python rerun_acr_k8.py
