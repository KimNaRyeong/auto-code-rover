# Hotswap - ACR Re-execution Workflow

이 디렉토리는 GCN 모델로 incorrect로 예측된 task들에 대해 ACR을 재실행하는 워크플로우를 포함합니다.

## 워크플로우 개요

1. **예측 단계**: k=8의 학습된 GCN 모델로 test set의 각 task에 대해 correctness 예측
2. **필터링 단계**: Incorrect (label=1)로 예측된 task들을 추출
3. **재사용 단계**: k=1~7까지는 기존 FL 결과를 재사용
4. **재실행 단계**: k=8에서 ACR을 5번 재실행 (gpt-4-0125-preview 사용)

## 파일 구조

```
hotswap/
├── README.md                       # 이 파일
├── predict_correctness.py          # Step 1: Correctness 예측
├── reuse_fl_results.py            # Step 2: k=1-7 FL 결과 재사용
├── rerun_acr_k8.py                # Step 3: k=8 ACR 재실행
├── run_full_workflow.sh           # 전체 워크플로우 실행
├── run_step1_predict.sh           # Step 1만 실행
├── run_step2_reuse.sh             # Step 2만 실행
├── run_step3_rerun.sh             # Step 3만 실행
├── predictions/                   # 예측 결과 저장 디렉토리
│   ├── k8_predictions.json        # 전체 예측 결과
│   └── k8_tasks_to_rerun.json     # 재실행할 task 목록
└── fl_outputs/                    # FL 재실행 결과 저장 디렉토리
    ├── rerun_output_1/            # 1번째 반복 결과
    ├── rerun_output_2/            # 2번째 반복 결과
    ├── rerun_output_3/            # 3번째 반복 결과
    ├── rerun_output_4/            # 4번째 반복 결과
    ├── rerun_output_5/            # 5번째 반복 결과
    ├── tasks_to_rerun.txt         # 재실행 task 목록 (텍스트)
    ├── copy_log.json              # FL 복사 로그
    └── acr_run_log.json           # ACR 실행 로그
```

## 사용법

### 전체 워크플로우 실행

```bash
cd /home/kimnal0/auto-code-rover/hotswap
./run_full_workflow.sh
```

### 개별 단계 실행

#### Step 1: Correctness 예측
```bash
./run_step1_predict.sh
```

출력:
- `predictions/k8_predictions.json`: 각 fold, task별 예측 결과 및 실제 label
- `predictions/k8_tasks_to_rerun.json`: Incorrect로 예측된 task 목록 (fold별)

#### Step 2: k=1-7 FL 결과 재사용
```bash
./run_step2_reuse.sh
```

기존 `/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_{1-5}`에서
k=1-7 결과를 `fl_outputs/rerun_output_{1-5}`로 복사

#### Step 3: k=8 ACR 재실행
```bash
./run_step3_rerun.sh
```

gpt-4-0125-preview 모델로 5번 반복 실행

## 주요 설정

### predict_correctness.py
- `k = 8`: 고정된 k 값
- `threshold = 0.5`: 예측 임계값
- `label_criteria = 1`: Label 기준
- `embedding_size = 300`: FastText 임베딩 크기

### rerun_acr_k8.py
- `model = "gpt-4-0125-preview"`: 사용할 LLM 모델
- `repetitions = 5`: 반복 횟수

## 입력 데이터

### 필요한 파일들
1. **Test set 정보**
   - `/home/kimnal0/auto-code-rover/atropos/results/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/test_bug_names2.json`

2. **학습된 모델**
   - `/home/kimnal0/auto-code-rover/atropos/trained_model/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/8/fold_{0-4}/best_auc.pt`

3. **Dataset**
   - `/home/kimnal0/auto-code-rover/atropos/data/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/8/gcn_dataset.pth`

4. **기존 FL 결과**
   - `/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_{1-5}/no_patch/`

## 출력 데이터

### predictions/k8_predictions.json
```json
{
    "0": {  // fold 번호
        "task_name": {
            "predicted_label": 0 or 1,
            "probability": 0.0-1.0,
            "actual_label": 0 or 1,
            "is_correct_prediction": true or false
        },
        ...
    },
    ...
}
```

### predictions/k8_tasks_to_rerun.json
```json
{
    "0": ["task1", "task2", ...],  // fold별 재실행 task 목록
    "1": [...],
    ...
}
```

### fl_outputs/acr_run_log.json
```json
{
    "model": "gpt-4-0125-preview",
    "k": 8,
    "total_tasks": 100,
    "tasks": ["task1", "task2", ...],
    "repetitions": {
        "1": {
            "success": true,
            "timestamp": "2024-01-01T00:00:00",
            "output_dir": "..."
        },
        ...
    }
}
```

## 주의사항

1. **환경 설정**: `pytorch` conda 환경이 필요합니다
2. **실행 시간**: Step 3 (ACR 재실행)은 task 수와 모델에 따라 매우 오래 걸릴 수 있습니다
3. **중간 저장**: 각 단계의 결과가 파일로 저장되므로 중간에 멈춰도 다음 단계부터 재개 가능
4. **디스크 공간**: FL 결과 복사로 인해 상당한 디스크 공간이 필요할 수 있습니다

## 트러블슈팅

### Python 환경 문제
```bash
# conda 환경 활성화 확인
conda activate pytorch
python --version
```

### 모델 파일이 없을 때
```bash
# 모델 파일 존재 확인
ls /home/kimnal0/auto-code-rover/atropos/trained_model/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/8/
```

### ACR 실행 실패
- `fl_outputs/rerun_output_{1-5}/logs/stderr.log` 확인
- API 키 설정 확인
- 모델 이름이 올바른지 확인

## 다음 단계

1. 5번의 실행 결과에 대해 majority voting 수행
2. 최종 FL 결과 집계
3. 성능 평가 및 분석

## 문의

문제가 있을 경우 로그 파일들을 확인하세요:
- `predictions/`: 예측 관련 로그
- `fl_outputs/copy_log.json`: FL 복사 로그
- `fl_outputs/acr_run_log.json`: ACR 실행 로그
- `fl_outputs/rerun_output_{1-5}/logs/`: 각 실행의 상세 로그
