#!/bin/bash

# Final Hotswap Workflow
# This script runs GPT-4 k=8 for tasks predicted as incorrect by the GCN model

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "======================================================================="
echo "HOTSWAP FINAL WORKFLOW"
echo "GPT-4 k=8 Execution + Result Comparison"
echo "======================================================================="
echo ""

# Activate conda environment
echo -e "${YELLOW}Activating conda environment...${NC}"
source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh
conda activate pytorch
echo -e "${GREEN}✓ Environment activated${NC}"
echo ""

# Step 1: Predict correctness
echo -e "${BLUE}Step 1: Predicting correctness for k=8 test set...${NC}"
cd /home/kimnal0/auto-code-rover/hotswap

if [ ! -f "predictions/k8_predictions.json" ]; then
    python predict_correctness.py
    echo -e "${GREEN}✓ Predictions completed${NC}"
else
    echo -e "${YELLOW}⚠ Predictions already exist, skipping...${NC}"
fi
echo ""

# Step 2: Prepare task list
echo -e "${BLUE}Step 2: Preparing task list for ACR...${NC}"
python prepare_task_list.py
echo -e "${GREEN}✓ Task list prepared${NC}"
echo ""

# Check if task list exists and is not empty
TASK_COUNT=$(wc -l < incorrect_tasks.txt)
echo -e "${GREEN}Total tasks to run: ${TASK_COUNT}${NC}"
echo ""

if [ "$TASK_COUNT" -eq 0 ]; then
    echo -e "${RED}No incorrect tasks found. Exiting.${NC}"
    exit 0
fi

# Step 3: Run GPT-4 k=8 (5 times)
echo -e "${BLUE}Step 3: Running GPT-4 k=8 (5 repetitions)...${NC}"
echo -e "${YELLOW}⚠ This will take a VERY long time and cost money!${NC}"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Aborted by user.${NC}"
    exit 1
fi

cd /home/kimnal0/auto-code-rover

for i in 1 2 3 4 5; do
    echo ""
    echo -e "${BLUE}Running repetition ${i}/5...${NC}"

    OUTPUT_DIR="hotswap/fl_outputs/gpt4_k8_run_${i}"

    PYTHONPATH=. python app/main.py swe-bench \
        --model gpt-4-0125-preview \
        --conv-round-limit 8 \
        --setup-map SWE-bench/setup_result/setup_map.json \
        --tasks-map SWE-bench/setup_result/tasks_map.json \
        --output-dir "${OUTPUT_DIR}" \
        --task-list-file hotswap/incorrect_tasks.txt

    echo -e "${GREEN}✓ Repetition ${i} completed${NC}"
done

echo ""
echo -e "${GREEN}✓ All 5 repetitions completed${NC}"
echo ""

# Step 4: Compare results
echo -e "${BLUE}Step 4: Comparing Mixtral k=7 vs GPT-4 k=8...${NC}"
cd /home/kimnal0/auto-code-rover/hotswap

python compare_results.py
echo -e "${GREEN}✓ Comparison completed${NC}"
echo ""

# Summary
echo "======================================================================="
echo -e "${GREEN}WORKFLOW COMPLETED${NC}"
echo "======================================================================="
echo ""
echo "Results saved in:"
echo "  - predictions/k8_predictions.json"
echo "  - predictions/k8_tasks_to_rerun.json"
echo "  - fl_outputs/gpt4_k8_run_{1-5}/"
echo "  - comparison_results.json"
echo ""
echo "Next steps:"
echo "  1. Review comparison_results.json"
echo "  2. Analyze Mixtral vs GPT-4 differences"
echo "  3. Evaluate cost vs accuracy improvement"
echo ""
