# Quick Start Guide

## 빠른 실행

전체 워크플로우를 한 번에 실행하려면:

```bash
cd /home/kimnal0/auto-code-rover/hotswap
./run_full_workflow.sh
```

## 단계별 실행

### Step 1: 예측 (Prediction)
k=8 모델로 test set의 correctness 예측

```bash
./run_step1_predict.sh
```

**결과 확인:**
```bash
cat predictions/k8_predictions.json | jq '."0" | length'  # fold 0의 task 수
cat predictions/k8_tasks_to_rerun.json | jq '."0" | length'  # fold 0에서 재실행할 task 수
```

### Step 2: FL 결과 재사용 (Reuse)
k=1-7의 기존 FL 결과를 복사

```bash
./run_step2_reuse.sh
```

**결과 확인:**
```bash
cat fl_outputs/copy_log.json | jq '.total_tasks'  # 재실행할 총 task 수
ls fl_outputs/rerun_output_1/no_patch/ | wc -l  # 복사된 task 수 (repetition 1)
```

### Step 3: ACR 재실행 (Re-run)
k=8에서 gpt-4-0125-preview로 5번 재실행

```bash
./run_step3_rerun.sh
```

**진행 상황 확인:**
```bash
# 실행 중일 때 로그 확인
tail -f fl_outputs/rerun_output_1/logs/stdout.log

# 완료 후 결과 확인
cat fl_outputs/acr_run_log.json | jq '.repetitions'
```

## 예상 실행 시간

- **Step 1 (예측)**: ~5분
- **Step 2 (재사용)**: ~10분 (task 수에 따라 다름)
- **Step 3 (재실행)**: 매우 긴 시간 (task당 5-10분 × task 수 × 5 반복)
  - 예: 100개 task → 약 50-100시간

## 출력 파일 요약

| 파일 | 설명 |
|------|------|
| `predictions/k8_predictions.json` | 전체 예측 결과 (fold별, task별) |
| `predictions/k8_tasks_to_rerun.json` | 재실행할 task 목록 |
| `fl_outputs/tasks_to_rerun.txt` | 재실행 task 목록 (텍스트) |
| `fl_outputs/copy_log.json` | FL 복사 통계 |
| `fl_outputs/acr_run_log.json` | ACR 실행 통계 |
| `fl_outputs/rerun_output_{1-5}/` | 각 반복의 FL 결과 |

## 자주 사용하는 명령어

```bash
# 전체 재실행할 task 수 확인
cat predictions/k8_tasks_to_rerun.json | jq '[.[]] | add | length'

# fold별 재실행 task 수
cat predictions/k8_tasks_to_rerun.json | jq 'to_entries | .[] | {fold: .key, count: (.value | length)}'

# 예측 정확도 확인
cat predictions/k8_predictions.json | jq '[.[] | .[] | .is_correct_prediction] | map(select(. == true)) | length'

# ACR 실행 상태 확인
cat fl_outputs/acr_run_log.json | jq '.repetitions | to_entries | .[] | {rep: .key, success: .value.success}'
```

## 중단 및 재개

각 단계는 독립적으로 실행 가능하므로, 중간에 중단되어도 완료된 단계는 다시 실행할 필요가 없습니다.

예를 들어, Step 2까지 완료하고 Step 3에서 중단된 경우:
```bash
# Step 3만 다시 실행
./run_step3_rerun.sh
```

## 주의사항

1. ⚠️ **Step 3는 매우 오래 걸립니다** - 백그라운드에서 실행하는 것을 권장
   ```bash
   nohup ./run_step3_rerun.sh > step3.log 2>&1 &
   ```

2. ⚠️ **API 비용** - gpt-4-0125-preview 사용으로 인한 비용 발생

3. ⚠️ **디스크 공간** - FL 결과가 크므로 충분한 공간 확보 필요

## 문제 해결

### conda 환경 활성화 실패
```bash
# conda 경로 확인
which conda

# 수동으로 환경 활성화
conda activate pytorch
```

### Python 모듈 없음
```bash
# pytorch 환경에서 필요한 패키지 확인
conda activate pytorch
pip list | grep torch
pip list | grep tqdm
```

### ACR 실행 실패
```bash
# 에러 로그 확인
cat fl_outputs/rerun_output_1/logs/stderr.log

# API 키 설정 확인
echo $OPENAI_API_KEY
```

## 다음 단계

1. ✅ 모든 단계 완료 후 majority voting 구현
2. ✅ 최종 FL 결과 집계
3. ✅ 성능 평가

더 자세한 내용은 [README.md](README.md)를 참조하세요.
