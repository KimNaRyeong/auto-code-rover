#!/bin/bash

# Activate conda environment and run prediction script
source ~/anaconda3/etc/profile.d/conda.sh || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch

echo "Running correctness prediction for k=8..."
cd /home/kimnal0/auto-code-rover/hotswap
python predict_correctness.py
