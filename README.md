# 기업 분석 및 마케팅 전략 보고서 자동화 시스템

기업명과 URL만 입력하면 자동으로 **고도화된 기업 분석 및 마케팅 전략 보고서**를 생성하는 Python 기반 자동화 도구입니다.

## 주요 기능

- **웹사이트 자동 스크래핑 및 분석**
- **11개 섹션으로 구성된 전문 보고서**
- **Plette Agent 기반 마케팅 자동화 제안**
- **DOCX 형식의 제안서 자동 생성**
- **Notion 페이지 연동 지원**

## 프로젝트 구조

```
jebaek_project/
├── src/
│   ├── main.py              # 메인 스크립트
│   ├── web_scraper.py       # 웹 스크래핑 모듈
│   ├── analyzer.py          # 기업 분석 모듈 (11개 섹션)
│   ├── docx_generator.py    # DOCX 생성 모듈
│   └── notion_generator.py  # Notion 연동 모듈
├── output/                  # 생성된 제안서 저장 폴더
├── examples/                # 예제 파일
├── requirements.txt         # 필요한 패키지 목록
└── README.md
```

## 보고서 구성 (11개 섹션)

### 1. 핵심 요약 (Executive Summary)
바쁜 의사결정권자를 위한 핵심 정리
- 개요, 핵심 발견사항, 제안 전략
- 기대 효과 및 투자 대비 효과(ROI)

### 2. 기업 개요
기업 정보, 웹사이트, 디지털 성숙도 평가

### 3. 핵심 사업 영역
- 주요 사업 및 산업 분류
- 수익 구조, 비즈니스 모델
- 핵심 가치 제안

### 4. 현재 타겟 시장 & 고객
- 시장 규모 및 주요 타겟
- 타겟 고객 세분화
- 고객 페르소나 정의

### 5. 경쟁사 분석
- 직접/간접 경쟁사 식별
- 경쟁사 마케팅 방식 분석
- 차별화 포인트 및 경쟁 우위 전략

### 6. 시장 및 고객 행동 분석
- 고객 페인포인트 식별
- 고객 의사결정 구조 맵핑
- 시장 트렌드 및 구매 여정 분석

### 7. 산업·업계 가치 + 기존 마케팅의 한계
**매우 중요: Agent 필요성 배경 섹션**
- 산업 가치 정의
- 기존 마케팅의 5가지 한계
- 디지털 전환 필요성
- Agent 도입 당위성

### 8. 온드미디어 중심 마케팅 전략 제안
- 블로그 & SEO 전략
- SNS 전략 (LinkedIn, Instagram, YouTube)
- 영상 콘텐츠 전략
- B2B Funnel 기반 전략 (TOFU/MOFU/BOFU)
- 통합 실행 계획

### 9. Plette Agent 활용 제안
- Agent 개요 및 기능
- 기존 한계 해결 방법
- Agent 기반 온드미디어 실행 구조
- 프로세스 및 비용 절감 효과
  - 인건비 60% 절감
  - 콘텐츠 제작 속도 10배 향상

### 10. 기대 효과 및 결론
- 단기/중기/장기 효과
- 정량적 목표 (ROI 300%)
- 정성적 가치

### 11. Next Step 제안 및 도입 로드맵
- 즉시 실행 사항
- 1/3/6/12개월 로드맵
- 투자 계획 및 성공 지표(KPI)

## 설치 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd jebaek_project
```

### 2. 가상환경 생성 (선택사항이지만 권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 사용 방법

### 방법 1: DOCX 파일만 생성 (기본)

#### 대화형 모드
```bash
cd src
python main.py
```

#### 커맨드라인 인자
```bash
cd src
python main.py "기업명" "https://example.com"
```

### 방법 2: DOCX + Notion 페이지 동시 생성

#### 1) Notion API 설정
Notion Integration을 생성하고 API 토큰을 발급받습니다:
1. https://www.notion.so/my-integrations 에서 Integration 생성
2. Internal Integration 선택
3. 생성된 Integration Token 복사
4. Notion에서 보고서를 생성할 페이지 선택 후 "···" → "Connections" → Integration 연결
5. 페이지 ID 복사 (URL에서 확인 가능)

#### 2) 환경변수 설정
```bash
export NOTION_TOKEN='secret_xxxxxxxxxxxx'
export NOTION_PARENT_PAGE_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

#### 3) 실행
```bash
cd src
python main.py "기업명" "https://example.com" --notion
```

또는 대화형 모드에서 Notion 출력 옵션 선택

### 예제

```bash
cd src

# DOCX만 생성
python main.py "삼성전자" "https://www.samsung.com"

# DOCX + Notion
python main.py "네이버" "https://www.naver.com" --notion
```

## 출력 결과

### DOCX 파일
생성된 제안서는 `output/` 디렉토리에 저장됩니다.

파일명 형식: `기업분석보고서_[기업명]_[타임스탬프].docx`

### Notion 페이지
설정된 부모 페이지 하위에 새로운 보고서 페이지가 생성됩니다.

## 필요 패키지

- **requests**: 웹 스크래핑
- **beautifulsoup4**: HTML 파싱
- **python-docx**: DOCX 문서 생성
- **lxml**: XML/HTML 처리
- **notion-client**: Notion API 연동

## 주요 특징

### 고도화된 분석
- 11개 섹션으로 구성된 전문 보고서
- 데이터 기반 인사이트 제공
- Plette Agent 활용 제안 포함

### Plette Agent 특징
- 24/7 무중단 콘텐츠 생성
- 인건비 대비 80-90% 비용 절감
- 콘텐츠 제작 속도 10배 향상
- 마케팅 ROI 300%+ 달성 가능

### 다양한 출력 형식
- DOCX: 전문적인 제안서 형식
- Notion: 협업 및 공유에 최적화

## Notion 연동 장점

1. **실시간 협업**: 팀원들과 보고서 공유 및 편집
2. **링크 공유**: URL 하나로 간편한 공유
3. **통합 관리**: 여러 보고서를 Notion에서 통합 관리
4. **자동 업데이트**: 보고서를 쉽게 수정 및 업데이트

## 주의사항

- 웹사이트에 따라 스크래핑이 제한될 수 있습니다
- robots.txt를 준수하여 사용하세요
- 과도한 요청은 IP 차단의 원인이 될 수 있습니다
- 생성된 제안서는 검토 후 사용하시기 바랍니다
- Notion API는 속도 제한(Rate Limit)이 있으므로 주의하세요

## 환경변수 설정 방법

### macOS / Linux
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export NOTION_TOKEN='your_notion_token'
export NOTION_PARENT_PAGE_ID='your_page_id'

# 적용
source ~/.bashrc  # 또는 source ~/.zshrc
```

### Windows (PowerShell)
```powershell
$env:NOTION_TOKEN='your_notion_token'
$env:NOTION_PARENT_PAGE_ID='your_page_id'
```

### Windows (CMD)
```cmd
set NOTION_TOKEN=your_notion_token
set NOTION_PARENT_PAGE_ID=your_page_id
```

## 문제 해결

### Notion 페이지 생성 실패
1. NOTION_TOKEN이 올바른지 확인
2. NOTION_PARENT_PAGE_ID가 정확한지 확인
3. Integration이 해당 페이지에 연결되어 있는지 확인
4. 페이지 권한 확인

### 웹 스크래핑 실패
- 기본 템플릿으로 제안서가 생성됩니다
- 네트워크 연결 확인
- URL이 유효한지 확인

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 문의

프로젝트 관련 문의사항은 이슈를 통해 남겨주세요.
