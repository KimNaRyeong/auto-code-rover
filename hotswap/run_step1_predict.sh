#!/bin/bash
# Step 1: Predict correctness for k=8

source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch

cd /home/kimnal0/auto-code-rover/hotswap
python predict_correctness.py
