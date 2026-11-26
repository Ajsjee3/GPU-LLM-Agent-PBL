# FinanceRAG

실제 기업 공시 자료를 기반으로 재무 정보 질의응답과 계산을 제공하는 AI Agent 개발 실습입니다. 현재는 평가 자동화 코드만 준비되었으며, RunPod의 기존 서비스 소스와 금융 문서 통합은 진행 예정입니다.

## 구성

- `evaluate.py`: HTTP 요청, 도구 선택 검증 및 응답 시간 측정
- `evaluation_config.json`: API 계약 및 테스트 설정 (초기값은 예시)
- `evaluation.ipynb`: Jupyter 실행용 노트북
- `app/`, `web/`: 기존 소스 통합 예정
- `data/`: 금융 자료 출처 기록
- `results/`, `screenshots/`: 실제 실행 결과 보관
- `docs/troubleshooting.md`: 오류 수정 기록

## 평가 방법

기존 FastAPI 서버가 실행 중인 RunPod에서 이 폴더로 이동한 후:

```bash
python -m pip install -r requirements.txt
python evaluate.py inspect
```

OpenAPI 및 기존 `tools.py`를 확인하여 `evaluation_config.json`의 endpoint, query_field, tool_field, success_field, expected_tool을 실제 값으로 수정합니다. API에 success 필드가 없다면 null로 변경합니다. 이 경우 성공 여부는 HTTP 성공과 도구 일치만 판단하며 답변 정확성은 별도로 확인합니다. 질문에 필요한 실제 문서가 등록되어 있어야 합니다.

```bash
python evaluate.py before
# 실패 원인 확인, 실제 소스 수정, 서버 재시작
python evaluate.py after
```

`before`는 전체 테스트 CSV와 첫 실패 항목을 저장합니다. `after`는 저장한 동일 질문과 설정으로 재측정합니다. 기존 before.csv가 있으면 별도 보관 후 새 실험을 시작합니다. 실패가 없다면 실제 경계 사례를 추가하고 실패를 조작하지 않습니다.

HTTP 테스트만으로 app.js 오류를 판단할 수 없습니다. 브라우저와 개발자 도구에서 같은 질문을 실행하고 실제 화면을 기록합니다. API 키 및 RunPod 토큰, 재배포 권한 없는 강의 자료는 커밋하지 않습니다.
