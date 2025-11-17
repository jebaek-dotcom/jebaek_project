"""
Multi-Agent 기반 고품질 보고서 생성 시스템

4개의 전문 Agent가 순차적으로 작업:
1. Researcher Agent: 정보 수집
2. Validator Agent: 검증 & 보완
3. Writer Agent: 구조화 & 작성
4. Reviewer Agent: 품질 검증
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict


class MultiAgentReportSystem:
    """Multi-Agent 보고서 생성 시스템"""

    def __init__(self, company_name: str, url: str):
        self.company_name = company_name
        self.url = url
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Agent별 작업 결과 저장
        self.research_data = {}      # Agent 1 결과
        self.validated_data = {}     # Agent 2 결과
        self.structured_content = {} # Agent 3 결과
        self.final_report = {}       # Agent 4 결과

    def stage1_research(self):
        """Stage 1: 정보수집 Agent"""
        print(f"\n{'='*60}")
        print(f"🔍 Stage 1: 정보수집 Agent (Researcher)")
        print(f"{'='*60}\n")

        research_prompt = f"""
        {self.company_name}에 대한 심층 조사를 수행하세요.

        **목표: 사실 기반의 정확한 정보 수집**

        다음 항목들을 WebSearch로 조사하세요:

        ## 1. 기업 기본정보
        - 설립 연도, 대표자, 본사 위치
        - 비전, 미션, 핵심 가치
        - 기업 연혁 (주요 마일스톤)

        ## 2. 사업 모델 심층 분석
        - 핵심 제품/서비스 상세
        - 수익 구조 (어떻게 돈을 버는가?)
        - 타겟 고객 (B2B/B2C/B2B2C)
        - 가치 제안 (고객에게 제공하는 가치)

        ## 3. 경쟁사 정확한 식별
        - 직접 경쟁사 3-5개 (같은 제품/서비스)
        - 각 경쟁사의 시장 점유율
        - 경쟁사 대비 차별점

        ## 4. 파트너십 & 투자
        - 주요 파트너사 (구체적 이름)
        - 투자 유치 현황
        - 정부 지원 프로그램 선정

        ## 5. 시장 데이터
        - 속한 업종의 시장 규모 (구체적 수치)
        - 성장률 및 전망
        - 주요 트렌드

        각 항목마다 **구체적인 사실과 수치**를 포함하세요.
        모호한 표현 대신 정확한 정보를 수집하세요.

        결과를 research_stage1.json에 저장하세요.
        """

        print(research_prompt)
        print("\n" + "="*60)
        print("💬 Claude Agent에게 위 프롬프트를 전달하고")
        print("   research_stage1.json 생성을 기다리세요.")
        print("="*60 + "\n")

        return research_prompt

    def stage2_validation(self):
        """Stage 2: 검증 & 보완 Agent"""
        print(f"\n{'='*60}")
        print(f"✅ Stage 2: 검증 & 보완 Agent (Validator)")
        print(f"{'='*60}\n")

        # research_stage1.json 읽기
        stage1_file = os.path.join(self.script_dir, 'research_stage1.json')
        if not os.path.exists(stage1_file):
            print("❌ research_stage1.json 파일이 없습니다!")
            return None

        with open(stage1_file, 'r', encoding='utf-8') as f:
            self.research_data = json.load(f)

        validation_prompt = f"""
        Stage 1에서 수집된 {self.company_name} 정보를 검증하고 보완하세요.

        **목표: 정보의 정확성과 완전성 확보**

        ## 검증 체크리스트

        ### 1. 일관성 검증
        - 서로 다른 출처의 정보가 일치하는가?
        - 모순되는 내용은 없는가?
        - 날짜, 수치가 정확한가?

        ### 2. 완전성 검증
        - 각 섹션이 충분히 구체적인가?
        - 누락된 중요 정보는 없는가?
        - "조사 중", "정보 없음" 항목 확인

        ### 3. 보완 작업
        누락되거나 불충분한 정보에 대해:
        - 추가 WebSearch 수행
        - 다른 키워드로 재검색
        - 관련 기사, 보도자료 확인

        ### 4. 경쟁사 검증
        - 정말 직접 경쟁사가 맞는가?
        - 시장 점유율 데이터가 정확한가?

        ### 5. 차별점 명확화
        - {self.company_name}만의 고유한 특징은?
        - 경쟁사와의 명확한 차이는?

        **검증 결과를 research_stage2_validated.json에 저장하세요.**

        각 항목마다:
        - verified: true/false
        - confidence: high/medium/low
        - notes: 검증 과정 노트
        를 추가하세요.
        """

        print(validation_prompt)
        print("\n" + "="*60)
        print("💬 Claude Agent에게 위 프롬프트를 전달하고")
        print("   research_stage2_validated.json 생성을 기다리세요.")
        print("="*60 + "\n")

        return validation_prompt

    def stage3_writing(self):
        """Stage 3: 구조화 & 작성 Agent"""
        print(f"\n{'='*60}")
        print(f"✍️  Stage 3: 구조화 & 작성 Agent (Writer)")
        print(f"{'='*60}\n")

        # research_stage2_validated.json 읽기
        stage2_file = os.path.join(self.script_dir, 'research_stage2_validated.json')
        if not os.path.exists(stage2_file):
            print("❌ research_stage2_validated.json 파일이 없습니다!")
            return None

        with open(stage2_file, 'r', encoding='utf-8') as f:
            self.validated_data = json.load(f)

        writing_prompt = f"""
        검증된 정보를 바탕으로 {self.company_name}의 마케팅 전략 보고서를 작성하세요.

        **목표: 맥락 있고 구체적인 전략 수립**

        ## 작성 원칙

        1. **구체성**: 일반론 금지, {self.company_name} 고유 특성 반영
        2. **맥락성**: 단순 나열이 아닌 논리적 연결
        3. **실행가능성**: 추상적 제안이 아닌 구체적 액션

        ## 11개 섹션 작성

        ### 1. Executive Summary
        - {self.company_name}가 **왜** 마케팅 전환이 필요한가? (구체적 이유)
        - 핵심 발견: {self.company_name}의 **실제** 현황 기반
        - 제안 전략: {self.company_name}에 **맞춤화된** 전략

        ### 2. 기업 개요
        - 단순 정보 나열 X
        - {self.company_name}의 **스토리** 중심
        - 파트너십이 의미하는 것, 성장 방향성

        ### 3. 핵심 사업 영역
        - NanuPay 같은 구체적 제품명 사용
        - 비즈니스 모델의 **독특함** 강조
        - 왜 이 사업이 중요한가?

        ### 4. 타겟 시장 & 고객
        - "B2B 기업"이 아니라 **어떤** B2B 기업인가?
        - 외국인 관광객, 면세점 등 **구체적** 타겟

        ### 5. 경쟁사 분석
        - 일반적인 이커머스가 아니라
        - **크로스보더 결제 시장**의 경쟁사
        - {self.company_name}의 차별점 명확히

        ### 6. 시장 행동 분석
        - 고객(외국인 관광객)이 **실제로** 어떻게 결제하는가?
        - 할부 결제가 왜 중요한가?

        ### 7. 산업 가치 + 마케팅 한계
        - 크로스보더 결제 시장의 가치
        - 기존 결제 방식의 한계
        - {self.company_name} 솔루션의 필요성

        ### 8. 온드미디어 전략
        - 핀테크/B2B2C 특성 반영
        - 업종 사례: 다른 핀테크 기업들은?
        - {self.company_name} 현황: 실제 채널 운영
        - 맞춤 전략: B2B(가맹점) + B2C(관광객)

        ### 9. Plette Agent 제안
        - {self.company_name}가 Agent를 쓰면 **구체적으로** 뭐가 좋은가?
        - 할부 결제 안내 콘텐츠 자동 생성
        - 다국어 마케팅 자동화

        ### 10. 기대 효과
        - {self.company_name}의 **실제** 목표 반영
        - 구체적 수치 (가맹점 수, 거래액 등)

        ### 11. 실행 로드맵
        - {self.company_name} 상황에 맞는 타임라인
        - 초기 스타트업 vs 성장기 차이

        ## 중요: 절대 하지 말아야 할 것

        ❌ "온라인 고객 접점 강화 필요" (너무 일반적)
        ✅ "외국인 관광객의 할부 결제 인지도 제고 필요" (구체적)

        ❌ "경쟁사: 이커머스 플랫폼들" (틀림)
        ✅ "경쟁사: 다른 크로스보더 결제 솔루션" (정확)

        ❌ "블로그 주 3회 발행" (일반론)
        ✅ "가맹점 사례, 할부 이용 가이드 발행" (맞춤)

        **결과를 research_stage3_content.json에 저장하세요.**
        """

        print(writing_prompt)
        print("\n" + "="*60)
        print("💬 Claude Agent에게 위 프롬프트를 전달하고")
        print("   research_stage3_content.json 생성을 기다리세요.")
        print("="*60 + "\n")

        return writing_prompt

    def stage4_review(self):
        """Stage 4: 품질 검증 Agent"""
        print(f"\n{'='*60}")
        print(f"🔍 Stage 4: 품질 검증 Agent (Reviewer)")
        print(f"{'='*60}\n")

        # research_stage3_content.json 읽기
        stage3_file = os.path.join(self.script_dir, 'research_stage3_content.json')
        if not os.path.exists(stage3_file):
            print("❌ research_stage3_content.json 파일이 없습니다!")
            return None

        with open(stage3_file, 'r', encoding='utf-8') as f:
            self.structured_content = json.load(f)

        review_prompt = f"""
        작성된 {self.company_name} 보고서를 최종 검증하세요.

        **목표: 고품질 보고서 보증**

        ## 검증 기준

        ### 1. 구체성 검증
        각 섹션을 읽고 체크:
        - [ ] {self.company_name} 고유 특성이 반영되었는가?
        - [ ] 일반적인 템플릿 표현이 남아있는가?
        - [ ] 실제 제품명, 파트너사명이 언급되는가?

        ### 2. 논리적 일관성
        - [ ] 섹션 간 연결이 자연스러운가?
        - [ ] 모순되는 내용은 없는가?
        - [ ] 전체 스토리가 설득력 있는가?

        ### 3. 전략 실행가능성
        - [ ] 제안된 전략이 {self.company_name} 상황에 맞는가?
        - [ ] 구체적 액션 아이템이 있는가?
        - [ ] 타임라인이 현실적인가?

        ### 4. 수치 검증
        - [ ] 시장 규모, 성장률이 정확한가?
        - [ ] ROI, 비용 절감 추정이 합리적인가?

        ### 5. 차별점 명확성
        - [ ] {self.company_name}의 경쟁 우위가 명확한가?
        - [ ] 왜 Agent가 필요한지 설득력 있는가?

        ## 개선 사항

        부족한 부분이 있다면:
        1. 구체적으로 무엇을 수정할지 명시
        2. 수정 이유 설명
        3. 수정안 제시

        ## 최종 승인

        모든 기준을 통과하면:
        - approved: true
        - final_report를 research_stage4_final.json에 저장

        통과하지 못하면:
        - approved: false
        - improvement_needed: [개선 필요 사항 리스트]
        - Stage 3로 돌아가서 재작성
        """

        print(review_prompt)
        print("\n" + "="*60)
        print("💬 Claude Agent에게 위 프롬프트를 전달하고")
        print("   research_stage4_final.json 생성을 기다리세요.")
        print("="*60 + "\n")

        return review_prompt

    def generate_docx(self):
        """최종 DOCX 생성"""
        print(f"\n{'='*60}")
        print(f"📄 DOCX 보고서 생성")
        print(f"{'='*60}\n")

        # research_stage4_final.json 읽기
        stage4_file = os.path.join(self.script_dir, 'research_stage4_final.json')
        if not os.path.exists(stage4_file):
            print("❌ research_stage4_final.json 파일이 없습니다!")
            return None

        with open(stage4_file, 'r', encoding='utf-8') as f:
            self.final_report = json.load(f)

        # 승인 여부 확인
        if not self.final_report.get('approved', False):
            print("❌ 보고서가 아직 승인되지 않았습니다!")
            print("   개선이 필요합니다:")
            for item in self.final_report.get('improvement_needed', []):
                print(f"   - {item}")
            return None

        # DOCX 생성 로직
        print("✅ 보고서가 승인되었습니다!")
        print("📝 DOCX 파일 생성 중...")

        from analyzer_research import ResearchBasedAnalyzer
        from docx_generator import ProposalGenerator

        # Analyzer에 최종 데이터 전달
        analyzer = ResearchBasedAnalyzer(
            self.company_name,
            {},  # homepage_data (필요시)
            self.final_report.get('content', {})
        )

        # DOCX 생성
        generator = ProposalGenerator(self.final_report.get('content', {}))

        output_dir = os.path.join(self.script_dir, '../output')
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"고품질보고서_{self.company_name}_{timestamp}.docx"
        filepath = os.path.join(output_dir, filename)

        generator.generate(filepath)

        filesize = os.path.getsize(filepath) / 1024

        print(f"\n✅ 완료!")
        print(f"📄 파일: {filepath}")
        print(f"📦 크기: {filesize:.2f} KB")
        print(f"\n💡 이 보고서는 4단계 검증을 거친 고품질 보고서입니다!\n")

        return filepath


def main():
    """메인 함수"""
    if len(sys.argv) < 4:
        print("\n❌ 사용법:")
        print("   python main_multiagent.py \"회사명\" \"URL\" <stage>\n")
        print("   stage: 1 (정보수집), 2 (검증), 3 (작성), 4 (검토), 5 (생성)\n")
        return

    company_name = sys.argv[1]
    url = sys.argv[2]
    stage = sys.argv[3]

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    system = MultiAgentReportSystem(company_name, url)

    if stage == '1':
        system.stage1_research()
    elif stage == '2':
        system.stage2_validation()
    elif stage == '3':
        system.stage3_writing()
    elif stage == '4':
        system.stage4_review()
    elif stage == '5':
        system.generate_docx()
    else:
        print(f"❌ 알 수 없는 stage: {stage}")
        print("   1, 2, 3, 4, 5 중 하나를 입력하세요.")


if __name__ == "__main__":
    main()
