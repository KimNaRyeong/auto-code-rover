# ACR Hotswap Analysis & Strategy

## 목표
- Mixtral로 k=1~7 실행 후 incorrect로 예측된 task를
- GPT-4로 k=8을 추가 실행했을 때 결과가 어떻게 달라지는지 확인

## 문제점 발견

### 1. ACR의 실행 구조
- `config.conv_round_limit` = k 값
- `agent_search.generator()`가 Python generator로 구현됨
- Generator의 내부 상태(메시지 히스토리, context 등)를 중간에 복원하는 것은 **매우 복잡함**

### 2. 시도한 방법들

#### 방법 1: Generator 상태 복원 (실패)
- 이전 round들을 "replay"해서 generator 상태 복원
- 문제: Generator 내부 상태가 복잡하고, 정확한 복원이 어려움
- 결론: 구현 복잡도가 너무 높고 버그 가능성 큼

#### 방법 2: 단순히 k=8로 재실행 (가능하지만 부정확)
- `--conv-round-limit 8`로 처음부터 다시 실행
- 문제: k=1~7의 결과가 이전과 달라질 수 있음 (LLM의 non-deterministic nature)
- 결론: "정확히 같은 k=1~7 + 새로운 k=8"이 아님

## 권장 해결책

### 최선의 방법: 비교 분석

k=1~7의 결과를 "재사용"하는 대신, **결과를 비교 분석**하는 것이 더 현실적입니다:

1. **Mixtral k=7 결과**: 이미 있음
   - `/fl_outputs/only_fl_output_mixtral_{1-5}`

2. **GPT-4 k=8 결과**: 새로 실행
   - `--model gpt-4-0125-preview --conv-round-limit 8`로 처음부터 실행
   - 5번 반복 실행

3. **비교 분석**:
   - Mixtral k=7에서 찾은 bug location
   - GPT-4 k=8에서 찾은 bug location
   - 둘의 차이점 분석
   - Round별 API call 패턴 비교

### 구체적인 실행 방법

```bash
# Incorrect로 예측된 task들에 대해
# GPT-4로 k=8 실행 (5번 반복)

for i in 1 2 3 4 5; do
    PYTHONPATH=. python app/main.py swe-bench \
        --model gpt-4-0125-preview \
        --conv-round-limit 8 \
        --setup-map SWE-bench/setup_result/setup_map.json \
        --tasks-map SWE-bench/setup_result/tasks_map.json \
        --output-dir hotswap/gpt4_k8_output_${i} \
        --task-list-file hotswap/predictions/incorrect_tasks.txt
done
```

### 비교 분석 스크립트

```python
# compare_results.py
# 1. Mixtral k=7의 FL 결과 로드
# 2. GPT-4 k=8의 FL 결과 로드
# 3. 각 round별로 비교:
#    - Round 0~6: Mixtral vs GPT-4 차이
#    - Round 7: GPT-4만 존재 (새로운 round)
# 4. Bug location 정확도 비교
```

## 결론

**Generator 상태 복원보다는 결과 비교 분석이 더 실용적입니다.**

이유:
1. ✅ 구현이 단순하고 확실함
2. ✅ 버그 없이 안정적으로 실행 가능
3. ✅ 실제로 원하는 정보(모델 차이에 따른 성능 변화)를 얻을 수 있음
4. ⚠️ k=1~7이 완전히 동일하지 않을 수 있음
   - 하지만: 5번 반복 실행 + majority voting으로 완화 가능
   - LLM은 기본적으로 non-deterministic하므로 "완전히 동일한 k=1~7"은 애초에 불가능

## 다음 단계

1. GCN 모델로 incorrect 예측된 task 목록 생성 ✅
2. GPT-4 k=8로 해당 task들 5번씩 실행
3. 결과 비교 분석 스크립트 작성
4. Mixtral k=7 vs GPT-4 k=8 성능 비교
