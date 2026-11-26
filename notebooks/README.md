# 실습 노트북

RunPod GPU 커널에서 순서대로 엽니다. 04·05는 노트북과 같은 저장소에 있는 앱 폴더를 사용하므로 저장소 전체를 복제하세요. 모델 캐시와 초기 실습 출력 디렉터리는 원래 RunPod 경로를 사용합니다.

| 순서 | 실습 | 살펴볼 내용 |
|---|---|---|
| 01 | [Qwen·Gemma GPU 추론](01_GPU_LLM_Qwen_Gemma.ipynb) | 생성 토큰 수, 소요 시간, 메모리 사용량 |
| 02 | [모델 평가](02_Model_Evaluation.ipynb) | 같은 질문에서 지시 준수와 JSON 형식 비교 |
| 03 | [Custom Tool Agent](03_Custom_Tool_Agent.ipynb) | 모델의 JSON 결정과 실제 실행된 도구 대조 |
| 04 | [FastAPI 서비스](04_FastAPI_Agent_Service.ipynb) | 도구 목록, 질문 처리, 입력 검증 |
| 05 | [Web MVP](05_AI_Agent_Web_MVP.ipynb) | 웹 리소스와 GPU 상태 확인, 정상·오류 질문 평가 |

모델 접근 승인이 필요한 경우 실습 환경에서 인증합니다. 제출본에는 콘솔 출력 대신 [측정 CSV](../results/)를 보관했고, 05의 마지막 평가표는 노트북에도 남겼습니다.
