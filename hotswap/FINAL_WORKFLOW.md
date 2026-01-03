# Final Hotswap Workflow

## 실행 전략

Generator 상태 복원이 너무 복잡하므로, **GPT-4로 k=8을 처음부터 실행**하고 **결과를 비교 분석**합니다.

## Step 1: Incorrect 예측된 Task 목록 생성

```bash
cd /home/kimnal0/auto-code-rover/hotswap
conda activate pytorch

# 예측 실행
python predict_correctness.py
```

출력: `predictions/k8_tasks_to_rerun.json`

## Step 2: GPT-4로 k=8 실행 (5번 반복)

```bash
cd /home/kimnal0/auto-code-rover

# Incorrect task 목록을 텍스트 파일로 변환
python hotswap/prepare_task_list.py

# 5번 반복 실행
for i in 1 2 3 4 5; do
    PYTHONPATH=. python app/main.py swe-bench \
        --model gpt-4-0125-preview \
        --conv-round-limit 8 \
        --setup-map SWE-bench/setup_result/setup_map.json \
        --tasks-map SWE-bench/setup_result/tasks_map.json \
        --output-dir hotswap/fl_outputs/gpt4_k8_run_${i} \
        --task-list-file hotswap/incorrect_tasks.txt
done
```

## Step 3: 결과 비교 분석

```bash
cd /home/kimnal0/auto-code-rover/hotswap
conda activate pytorch

# Mixtral k=7 vs GPT-4 k=8 비교
python compare_results.py
```

## 비교 분석 내용

1. **Round별 API Call 패턴**
   - Round 0-6: Mixtral vs GPT-4 차이
   - Round 7: GPT-4의 새로운 정보 활용

2. **Bug Location 정확도**
   - Mixtral k=7: 기존 결과
   - GPT-4 k=8: 새 결과
   - 정답 대비 각각의 정확도

3. **비용 대비 효과**
   - GPT-4 추가 실행 비용
   - 정확도 향상 정도
   - ROI 분석

## 예상 결과

- **Case 1**: GPT-4 k=8이 더 정확한 bug location 찾음
  → 모델 품질이 중요함을 확인

- **Case 2**: Round 7이 큰 차이를 만들지 못함
  → k=7이면 충분함을 확인

- **Case 3**: GPT-4의 Round 0-6도 더 좋음
  → k보다 모델이 더 중요함을 확인

## 장점

✅ 구현이 단순하고 안정적
✅ 실제로 원하는 인사이트 획득 가능
✅ 완전히 독립적인 실행으로 재현 가능

## 단점

⚠️ k=1~7이 완전히 동일하지 않을 수 있음
→ 하지만: 5번 반복 + majority voting으로 완화
