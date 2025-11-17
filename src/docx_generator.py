"""
DOCX 제안서 생성 모듈
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import Dict, List
import os


class ProposalGenerator:
    def __init__(self, analysis_data: Dict):
        self.data = analysis_data
        self.doc = Document()
        self._setup_styles()

    def _setup_styles(self):
        """문서 스타일 설정"""
        # 기본 폰트 설정
        style = self.doc.styles['Normal']
        font = style.font
        font.name = '맑은 고딕'
        font.size = Pt(11)

    def generate(self, output_path: str) -> str:
        """
        제안서 생성
        """
        # 표지
        self._add_cover_page()

        # 페이지 나누기
        self.doc.add_page_break()

        # 목차 (간단한 버전)
        self._add_table_of_contents()
        self.doc.add_page_break()

        # 경영진 요약
        self._add_executive_summary()
        self.doc.add_page_break()

        # 기업 개요
        self._add_company_overview()
        self.doc.add_page_break()

        # 산업 분석
        self._add_industry_analysis()

        # 경쟁 우위
        self._add_competitive_advantages()
        self.doc.add_page_break()

        # 타겟 고객
        self._add_target_audience()

        # 디지털 입지 분석
        self._add_digital_presence()
        self.doc.add_page_break()

        # 마케팅 전략
        self._add_marketing_strategies()
        self.doc.add_page_break()

        # 권장사항
        self._add_recommendations()

        # 다음 단계
        self._add_next_steps()
        self.doc.add_page_break()

        # 결론
        self._add_conclusion()

        # 저장
        self.doc.save(output_path)
        return output_path

    def _add_cover_page(self):
        """표지 페이지"""
        # 제목
        title = self.doc.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title.add_run(f'\n\n\n\n마케팅 전략 제안서\n\n')
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)

        # 부제목
        subtitle = self.doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = subtitle.add_run(f'{self.data.get("company_name", "기업명")}\n')
        run.font.size = Pt(20)
        run.font.bold = True

        # 날짜
        date_para = self.doc.add_paragraph()
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = date_para.add_run(f'\n\n\n{datetime.now().strftime("%Y년 %m월 %d일")}')
        run.font.size = Pt(14)

    def _add_table_of_contents(self):
        """목차"""
        heading = self.doc.add_heading('목차', level=1)
        heading.alignment = WD_ALIGN_PARAGRAPH.LEFT

        toc_items = [
            '1. 경영진 요약',
            '2. 기업 개요',
            '3. 산업 및 시장 분석',
            '4. 경쟁 우위 요소',
            '5. 타겟 고객 분석',
            '6. 디지털 입지 현황',
            '7. 마케팅 전략 제안',
            '8. 권장 사항',
            '9. 실행 계획 및 다음 단계',
            '10. 결론'
        ]

        for item in toc_items:
            p = self.doc.add_paragraph(item, style='List Number')
            p.paragraph_format.left_indent = Inches(0.5)

    def _add_executive_summary(self):
        """경영진 요약"""
        self.doc.add_heading('1. 경영진 요약', level=1)

        summary = self.data.get('executive_summary', '')
        self.doc.add_paragraph(summary)

    def _add_company_overview(self):
        """기업 개요"""
        self.doc.add_heading('2. 기업 개요', level=1)

        overview = self.data.get('company_overview', {})

        if overview:
            for key, value in overview.items():
                p = self.doc.add_paragraph()
                p.add_run(f'{key}: ').bold = True
                p.add_run(str(value))
        else:
            self.doc.add_paragraph('기업 정보를 수집 중입니다.')

    def _add_industry_analysis(self):
        """산업 분석"""
        self.doc.add_heading('3. 산업 및 시장 분석', level=1)

        industry = self.data.get('industry_analysis', '')
        self.doc.add_paragraph(industry)

        # 추가 설명
        self.doc.add_paragraph(
            '\n현재 디지털 마케팅 시장은 빠르게 성장하고 있으며, '
            '기업들은 온라인 채널을 통한 고객 확보에 주력하고 있습니다. '
            '데이터 기반 마케팅과 개인화된 고객 경험이 핵심 트렌드로 자리잡고 있습니다.'
        )

    def _add_competitive_advantages(self):
        """경쟁 우위"""
        self.doc.add_heading('4. 경쟁 우위 요소', level=1)

        self.doc.add_paragraph(
            '웹사이트 분석을 통해 식별된 주요 강점은 다음과 같습니다:'
        )

        advantages = self.data.get('competitive_advantages', [])
        for advantage in advantages:
            self.doc.add_paragraph(advantage, style='List Bullet')

    def _add_target_audience(self):
        """타겟 고객"""
        self.doc.add_heading('5. 타겟 고객 분석', level=1)

        target = self.data.get('target_audience', '')
        self.doc.add_paragraph(target)

        self.doc.add_paragraph(
            '\n\n효과적인 마케팅 캠페인을 위해서는 타겟 고객의 니즈, 행동 패턴, '
            '그리고 의사결정 과정을 깊이 이해해야 합니다. '
            '페르소나 개발과 고객 여정 맵핑을 통해 더욱 정교한 타겟팅이 가능합니다.'
        )

    def _add_digital_presence(self):
        """디지털 입지"""
        self.doc.add_heading('6. 디지털 입지 현황', level=1)

        digital = self.data.get('digital_presence', {})

        if digital:
            for key, value in digital.items():
                p = self.doc.add_paragraph()
                p.add_run(f'{key}\n').bold = True
                p.add_run(str(value))
                p.add_run('\n')
        else:
            self.doc.add_paragraph('디지털 입지 분석 중입니다.')

    def _add_marketing_strategies(self):
        """마케팅 전략"""
        self.doc.add_heading('7. 마케팅 전략 제안', level=1)

        self.doc.add_paragraph(
            '다음은 귀사의 마케팅 목표 달성을 위해 제안하는 핵심 전략들입니다:'
        )

        strategies = self.data.get('marketing_strategies', [])

        for i, strategy in enumerate(strategies, 1):
            self.doc.add_heading(f'7.{i} {strategy.get("전략", "")}', level=2)

            p = self.doc.add_paragraph()
            p.add_run('개요: ').bold = True
            p.add_run(strategy.get('설명', ''))

            p = self.doc.add_paragraph()
            p.add_run('실행 방안: ').bold = True
            p.add_run(strategy.get('실행방안', ''))

            self.doc.add_paragraph()  # 간격

    def _add_recommendations(self):
        """권장사항"""
        self.doc.add_heading('8. 권장 사항', level=1)

        self.doc.add_paragraph(
            '성공적인 마케팅 캠페인 실행을 위해 다음 사항들을 권장합니다:'
        )

        recommendations = self.data.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            self.doc.add_paragraph(f'{i}. {rec}', style='List Number')

    def _add_next_steps(self):
        """다음 단계"""
        self.doc.add_heading('9. 실행 계획 및 다음 단계', level=1)

        self.doc.add_paragraph(
            '제안된 마케팅 전략의 체계적인 실행을 위한 단계별 계획입니다:'
        )

        steps = self.data.get('next_steps', [])

        for step in steps:
            self.doc.add_heading(step.get('단계', ''), level=2)

            p = self.doc.add_paragraph()
            p.add_run('목표: ').bold = True
            p.add_run(step.get('내용', ''))

            p = self.doc.add_paragraph()
            p.add_run('세부 사항: ').bold = True
            p.add_run(step.get('세부사항', ''))

            self.doc.add_paragraph()

    def _add_conclusion(self):
        """결론"""
        self.doc.add_heading('10. 결론', level=1)

        conclusion = f"""
본 제안서는 {self.data.get('company_name', '귀사')}의 디지털 마케팅 역량 강화를 위한
종합적인 전략을 제시하였습니다.

제안된 전략들은 현재의 디지털 환경과 시장 트렌드를 반영하여 수립되었으며,
체계적인 실행을 통해 다음과 같은 성과를 기대할 수 있습니다:

• 온라인 가시성 및 브랜드 인지도 향상
• 웹사이트 트래픽 증가
• 리드 생성 및 전환율 개선
• 고객 참여도 향상
• ROI 측정 가능한 마케팅 체계 구축

성공적인 디지털 마케팅은 지속적인 모니터링과 최적화를 필요로 합니다.
제안된 전략을 단계적으로 실행하고, 데이터를 기반으로 지속적으로 개선해 나간다면
목표한 성과를 달성할 수 있을 것입니다.

추가 논의나 상세한 실행 계획 수립을 위해 언제든지 연락 주시기 바랍니다.
        """

        self.doc.add_paragraph(conclusion)

        # 감사 인사
        thanks = self.doc.add_paragraph('\n\n감사합니다.')
        thanks.alignment = WD_ALIGN_PARAGRAPH.RIGHT
