#!/bin/bash

# Master script to run the full hotswap workflow
# This script will:
# 1. Predict correctness for k=8 test set
# 2. Filter tasks predicted as incorrect
# 3. Reuse FL results from k=1-7
# 4. Re-run ACR for k=8 (5 times)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================="
echo "HOTSWAP WORKFLOW - ACR Re-execution for Incorrect Predictions"
echo "======================================================================="
echo ""

# Activate conda environment
echo -e "${YELLOW}Step 0: Activating conda environment...${NC}"
source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch
echo -e "${GREEN}✓ Conda environment activated${NC}"
echo ""

# Change to hotswap directory
cd /home/kimnal0/auto-code-rover/hotswap

# Step 1: Run predictions
echo -e "${YELLOW}Step 1: Predicting correctness for k=8 test set...${NC}"
python predict_correctness.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Predictions completed successfully${NC}"
else
    echo -e "${RED}✗ Prediction failed${NC}"
    exit 1
fi
echo ""

# Step 2: Reuse FL results from k=1-7
echo -e "${YELLOW}Step 2: Reusing FL results from k=1-7...${NC}"
python reuse_fl_results.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ FL results reused successfully${NC}"
else
    echo -e "${RED}✗ FL results reuse failed${NC}"
    exit 1
fi
echo ""

# Step 3: Re-run ACR for k=8
echo -e "${YELLOW}Step 3: Re-running ACR for k=8 (5 repetitions)...${NC}"
echo -e "${YELLOW}This may take a long time...${NC}"
python rerun_acr_k8.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ ACR re-run completed${NC}"
else
    echo -e "${RED}✗ ACR re-run failed${NC}"
    exit 1
fi
echo ""

# Summary
echo "======================================================================="
echo -e "${GREEN}WORKFLOW COMPLETED SUCCESSFULLY${NC}"
echo "======================================================================="
echo ""
echo "Output locations:"
echo "  - Predictions: /home/kimnal0/auto-code-rover/hotswap/predictions/"
echo "  - FL outputs: /home/kimnal0/auto-code-rover/hotswap/fl_outputs/"
echo ""
echo "Next steps:"
echo "  1. Check predictions in predictions/k8_predictions.json"
echo "  2. Review FL outputs in fl_outputs/rerun_output_*/"
echo "  3. Run majority voting on the 5 repetitions"
echo ""
