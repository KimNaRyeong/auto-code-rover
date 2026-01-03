# Hotswap - Mixtral vs GPT-4 FL Performance Comparison

## 개요

GCN 모델이 incorrect로 예측한 task들에 대해, Mixtral (k=7) vs GPT-4 (k=8)의 FL 성능을 비교합니다.

## 핵심 전략 변경

### 초기 계획 (실패)
- Mixtral k=1~7 결과를 "재사용"하고 GPT-4로 k=8만 추가 실행
- **문제**: Python generator 상태 복원이 매우 복잡하고 불안정

### 최종 전략 (성공)
- GPT-4로 k=8을 **처음부터** 실행 (5번 반복)
- Mixtral k=7 vs GPT-4 k=8 **결과 비교 분석**
- **장점**: 구현 단순, 안정적, 실제 필요한 인사이트 획득 가능

## 파일 구조

```
hotswap/
├── README_FINAL.md                 # 이 파일
├── ANALYSIS.md                     # 문제 분석 및 해결 과정
├── FINAL_WORKFLOW.md               # 최종 워크플로우 설명
├── predict_correctness.py          # GCN 모델로 correctness 예측
├── prepare_task_list.py            # Task 목록 준비
├── compare_results.py              # Mixtral vs GPT-4 비교
├── run_final_workflow.sh           # 전체 워크플로우 실행
├── predictions/                    # 예측 결과
│   ├── k8_predictions.json
│   ├── k8_tasks_to_rerun.json
│   └── fold_info.json
├── fl_outputs/                     # GPT-4 k=8 실행 결과
│   ├── gpt4_k8_run_1/
│   ├── gpt4_k8_run_2/
│   ├── gpt4_k8_run_3/
│   ├── gpt4_k8_run_4/
│   └── gpt4_k8_run_5/
└── comparison_results.json         # 비교 분석 결과
```

## 실행 방법

### 전체 워크플로우 실행

```bash
cd /home/kimnal0/auto-code-rover/hotswap
./run_final_workflow.sh
```

### 단계별 실행

#### Step 1: Correctness 예측
```bash
conda activate pytorch
cd /home/kimnal0/auto-code-rover/hotswap
python predict_correctness.py
```

#### Step 2: Task 목록 준비
```bash
python prepare_task_list.py
```

#### Step 3: GPT-4 k=8 실행 (5번)
```bash
cd /home/kimnal0/auto-code-rover

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

#### Step 4: 결과 비교
```bash
cd /home/kimnal0/auto-code-rover/hotswap
python compare_results.py
```

## 비교 분석 내용

### 1. Round별 비교
- **Round 0-6**: Mixtral vs GPT-4 API call 패턴
- **Round 7**: GPT-4의 추가 round (Mixtral은 k=7까지만)

### 2. Bug Location 정확도
- 각 모델이 찾은 bug location 개수
- 정답 대비 정확도 (developer patch와 비교)

### 3. 실행 통계
- 평균 round 수
- 평균 bug location 수
- API call 빈도 분석

## 예상 결과 및 인사이트

### Case 1: GPT-4 k=8 >> Mixtral k=7
- **의미**: 모델 품질이 매우 중요
- **행동**: GPT-4 사용 정당화

### Case 2: GPT-4 k=8 ≈ Mixtral k=7
- **의미**: k=7이면 충분, 추가 round는 큰 도움 안됨
- **행동**: Mixtral k=7 사용으로 비용 절감

### Case 3: GPT-4 Round 0-6도 Mixtral보다 우수
- **의미**: k보다 모델 품질이 더 중요
- **행동**: k를 늘리기보다 더 좋은 모델 사용

## 주의사항

### 비용
⚠️ GPT-4-0125-preview는 비싼 모델입니다
- Task당 5-10분 × task 수 × 5 반복
- 예상 비용을 미리 계산하세요

### 실행 시간
⚠️ 매우 오래 걸립니다
- 100개 task 기준: 50-100시간 예상
- 백그라운드 실행 권장: `nohup ./run_final_workflow.sh > workflow.log 2>&1 &`

### k=1~7 비동일성
⚠️ Mixtral과 GPT-4의 k=1~7이 완전히 동일하지 않음
- LLM은 기본적으로 non-deterministic
- 5번 반복 + majority voting으로 완화
- 완벽한 비교보다는 **경향성 파악**에 초점

## 트러블슈팅

### API 키 설정
```bash
export OPENAI_API_KEY="your-api-key"
```

### Conda 환경 문제
```bash
conda activate pytorch
python --version  # Python 3.9+ 확인
pip list | grep torch  # PyTorch 확인
```

### 결과 파일 없음
```bash
# Mixtral 결과 확인
ls /home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_1/no_patch/

# GPT-4 결과 확인
ls /home/kimnal0/auto-code-rover/hotswap/fl_outputs/gpt4_k8_run_1/no_patch/
```

## 참고 문서

- [ANALYSIS.md](ANALYSIS.md) - 문제 분석 및 해결 과정
- [FINAL_WORKFLOW.md](FINAL_WORKFLOW.md) - 상세한 워크플로우
- [QUICKSTART.md](QUICKSTART.md) - 빠른 시작 (구버전)

## 결론

Generator 상태 복원보다 **독립적인 실행 + 결과 비교**가 더 실용적입니다.

✅ 구현 단순
✅ 안정적 실행
✅ 실제 필요한 인사이트 획득 가능
✅ 완전한 재현성

비록 k=1~7이 완전히 동일하지 않지만, **모델 간 성능 차이와 k값의 영향**을 분석하기에는 충분합니다.
