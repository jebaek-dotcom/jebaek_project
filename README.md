# 마케팅 제안서 자동화 시스템

기업명과 URL만 입력하면 자동으로 마케팅 전략 제안서를 생성하는 Python 기반 자동화 도구입니다.

## 주요 기능

- 웹사이트 자동 스크래핑 및 분석
- 기업 정보 및 산업 분석
- 타겟 고객 및 경쟁 우위 식별
- 맞춤형 마케팅 전략 제안
- 전문적인 DOCX 형식의 제안서 자동 생성

## 프로젝트 구조

```
jebaek_project/
├── src/
│   ├── main.py              # 메인 스크립트
│   ├── web_scraper.py       # 웹 스크래핑 모듈
│   ├── analyzer.py          # 기업 분석 모듈
│   └── docx_generator.py    # DOCX 생성 모듈
├── output/                  # 생성된 제안서 저장 폴더
├── examples/                # 예제 파일
├── requirements.txt         # 필요한 패키지 목록
└── README.md
```

## 설치 방법

1. 저장소 클론
```bash
git clone <repository-url>
cd jebaek_project
```

2. 가상환경 생성 (선택사항이지만 권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 사용 방법

### 방법 1: 대화형 모드

```bash
cd src
python main.py
```

프로그램이 실행되면 다음 정보를 입력하세요:
- 기업명
- 기업 웹사이트 URL

### 방법 2: 커맨드라인 인자

```bash
cd src
python main.py "기업명" "https://example.com"
```

### 예제

```bash
cd src
python main.py "삼성전자" "https://www.samsung.com"
python main.py "네이버" "https://www.naver.com"
```

## 출력 결과

생성된 제안서는 `output/` 디렉토리에 저장됩니다.

파일명 형식: `마케팅제안서_[기업명]_[타임스탬프].docx`

## 제안서 포함 내용

1. 표지
2. 목차
3. 경영진 요약
4. 기업 개요
5. 산업 및 시장 분석
6. 경쟁 우위 요소
7. 타겟 고객 분석
8. 디지털 입지 현황
9. 마케팅 전략 제안 (SEO, 콘텐츠, 소셜미디어, 이메일, 퍼포먼스 마케팅)
10. 권장 사항
11. 실행 계획 및 다음 단계
12. 결론

## 필요 패키지

- requests: 웹 스크래핑
- beautifulsoup4: HTML 파싱
- python-docx: DOCX 문서 생성
- lxml: XML/HTML 처리

## 주의사항

- 웹사이트에 따라 스크래핑이 제한될 수 있습니다
- robots.txt를 준수하여 사용하세요
- 과도한 요청은 IP 차단의 원인이 될 수 있습니다
- 생성된 제안서는 검토 후 사용하시기 바랍니다

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!
