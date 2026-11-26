# FinanceRAG

삼성전자 2024년 2·3분기 실적을 비교하는 재무 질의응답 실습입니다. 예를 들어 “3분기 매출이 늘었는데 영업이익은 왜 줄었나요?”라고 물으면 검색에 사용한 문단과 공식 발표 링크를 답변 아래에서 열 수 있습니다. 기간과 단위는 [금융 자료](data/README.md)에서 확인할 수 있습니다.

### 실행

저장소 루트에서 아래 명령을 실행한 뒤 [로컬 웹 화면](http://127.0.0.1:8000)을 엽니다. CPU에서는 관련 문단을 발췌합니다.

```bash
python -m pip install -r FinanceRAG/requirements.txt
cd FinanceRAG/app
python -m uvicorn app:preview --factory --port 8000
```

강의 GPU에서는 [FinanceRAG.ipynb](app/FinanceRAG.ipynb)를 같은 폴더의 새 커널에서 위에서부터 실행합니다. 기본 강의 경로는 `/workspace/course`이며 `COURSE_ROOT`로 바꿀 수 있습니다. 강의의 모델 로더와 하이브리드 검색을 사용하고 금융 프롬프트, 출처 연결, 실측 응답 시간 및 웹 UI를 추가했습니다. 같은 본체에 맞는 강의 LoRA를 선택해 둔 경우 기본 모델과 응답을 비교할 수 있습니다. 이 저장소에 별도 어댑터 가중치는 없습니다. [강의 코드](https://github.com/elliediaz/llm26-course)

### 검증

`FinanceRAG/app`에서 `python -m unittest -v`를 실행합니다. 분기별 검색, 검색 결과 없음, 공백·길이 제한, 어댑터 없음, 엔진 실패 응답을 점검합니다. GPU 생성 품질과 LoRA 효과는 별도 측정이 필요합니다.

### 도구 선택 평가 스크립트

기존 [평가 노트북](evaluation.ipynb)과 [평가 코드](evaluate.py)는 [05 Web MVP](../05_agent_web_mvp)의 `POST /agent`를 평가합니다. 이 챗봇의 재무 질의 경로는 `POST /api/chat`입니다. 두 서버를 같은 포트에서 동시에 실행할 수 없으므로 평가 대상 서버를 먼저 선택합니다.

05 서버를 시작한 후 `FinanceRAG`에서 `python evaluate.py inspect`로 API를 확인하고 `python evaluate.py before`로 도구 선택을 평가합니다. 실패 사례가 저장되면 수정 후 `python evaluate.py after`로 같은 질문을 비교합니다. 결과 파일은 `results/`에 생성됩니다.
