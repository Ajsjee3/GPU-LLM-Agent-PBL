# GPU 기반 오픈소스 LLM·AI Agent 서비스 개발 PBL

RunPod에서 Qwen과 Gemma를 같은 질문으로 비교하고, Qwen이 계산·글자 수·현재 시각·기초 통계 도구를 선택하는 과정을 FastAPI와 웹 화면까지 연결했습니다. 별도 응용인 **FinanceRAG**에서는 삼성전자 실적 발표를 검색하고 답변의 근거를 확인할 수 있습니다.

## 어디서 시작할까요?

| 보고 싶은 내용 | 코드와 기록 |
|---|---|
| 모델 실행부터 도구 호출까지 따라가기 | [01~05 실습 노트북](notebooks/README.md) |
| FastAPI 요청과 응답 살펴보기 | [04 Agent 백엔드](04_agent_web_mvp/) |
| 브라우저에서 도구 선택 실험하기 | [05 Agent Web MVP](05_agent_web_mvp/) |
| 실제 기업 재무 자료로 질문하기 | [FinanceRAG 실행 방법](FinanceRAG/README.md) · [삼성전자 자료 출처](FinanceRAG/data/README.md) |

## 실습에서 확인한 점

- **모델 비교** — 저장한 질문 5개씩의 평가에서 Qwen3-8B와 Gemma-3-4B-IT의 지시 준수율은 각각 80%였습니다. 평균 생성 속도는 각각 30.48, 19.31 tokens/s였고 평균 최대 GPU 메모리는 15.28, 8.04 GB였습니다. 질문별 응답과 집계값을 함께 보관했습니다. [개별 응답](results/02_model_evaluation_results.csv) · [집계](results/02_model_selection_summary.csv)
- **도구 선택** — 03 실습과 05 웹 평가에서 모두 현재 시각 질문을 처리하지 못했습니다. 05에서는 서버가 HTTP 200을 반환했지만 선택한 도구가 비어 있었습니다. 계산, 글자 수, 통계, 일반 설명, 빈 입력 검증은 기대 동작과 일치했습니다. 빈 입력의 기대 응답은 422입니다. [03 실행 기록](results/03_agent_tool_execution_log.csv) · [05 평가표](results/05_mvp_evaluation.csv)
- **금융 자료 검색** — 삼성전자 2024년 2·3분기 자료에 출처와 발표일을 연결했습니다. CPU에서는 발췌 검색을 실행할 수 있고 강의 GPU에서는 하이브리드 검색 결과를 LLM에 전달합니다. 기본 모델과 LoRA의 답변 비교는 GPU 노트북에서 실행합니다. [재무 분석 노트북](FinanceRAG/app/FinanceRAG.ipynb)

01~05 결과는 저장된 실습 기록입니다. 05 CSV는 마지막으로 실행한 노트북의 표시 표에서 옮겼으며, 화면에서 축약된 오류 문자열은 그대로 남겼습니다. 이번 정리에서는 FinanceRAG CPU 테스트 5건을 다시 실행했습니다. GPU 모델 재추론 및 오류 수정 전후 재측정은 수행하지 않았습니다.
