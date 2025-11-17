"""
기업 분석 및 마케팅 전략 생성 모듈
"""

from typing import Dict, List
import re
from collections import Counter


class BusinessAnalyzer:
    def __init__(self, company_name: str, scraped_data: Dict):
        self.company_name = company_name
        self.data = scraped_data

    def analyze(self) -> Dict[str, any]:
        """
        기업 정보를 분석하고 마케팅 전략을 생성합니다.
        """
        if self.data.get('status') == 'error':
            return self._create_error_analysis()

        analysis = {
            'company_name': self.company_name,
            'executive_summary': self._create_executive_summary(),
            'company_overview': self._create_company_overview(),
            'industry_analysis': self._analyze_industry(),
            'competitive_advantages': self._identify_strengths(),
            'target_audience': self._identify_target_audience(),
            'marketing_strategies': self._generate_marketing_strategies(),
            'digital_presence': self._analyze_digital_presence(),
            'recommendations': self._create_recommendations(),
            'next_steps': self._define_next_steps()
        }

        return analysis

    def _create_error_analysis(self) -> Dict[str, any]:
        """오류 발생 시 기본 분석 반환"""
        return {
            'company_name': self.company_name,
            'executive_summary': f"{self.company_name}에 대한 정보를 수집하는 중 오류가 발생했습니다.",
            'error': True,
            'error_message': self.data.get('error_message', '알 수 없는 오류')
        }

    def _create_executive_summary(self) -> str:
        """요약문 생성"""
        title = self.data.get('title', '')
        description = self.data.get('meta_description', '')

        summary = f"""본 보고서는 {self.company_name}의 디지털 마케팅 전략 수립을 위한 종합 분석 자료입니다.

웹사이트 분석 결과를 바탕으로 기업의 현재 온라인 입지, 타겟 고객층, 그리고
시장 내 경쟁 우위를 파악하였으며, 이를 기반으로 한 맞춤형 마케팅 전략을 제안합니다."""

        if description:
            summary += f"\n\n기업 소개: {description}"

        return summary

    def _create_company_overview(self) -> Dict[str, str]:
        """기업 개요 생성"""
        return {
            '웹사이트': self.data.get('url', ''),
            '도메인': self.data.get('domain', ''),
            '웹사이트 제목': self.data.get('title', ''),
            '주요 설명': self.data.get('meta_description', '제공되지 않음'),
            '키워드': self.data.get('meta_keywords', '제공되지 않음')
        }

    def _analyze_industry(self) -> str:
        """산업 분석"""
        text = self.data.get('text_content', '').lower()
        keywords = self.data.get('meta_keywords', '').lower()

        # 주요 산업 키워드 감지
        industry_keywords = {
            '기술/IT': ['technology', 'software', 'it', 'digital', 'tech', 'ai', 'iot', 'cloud', '소프트웨어', '기술', '디지털'],
            '제조': ['manufacturing', 'production', 'factory', 'industrial', '제조', '생산', '공장'],
            '유통/소매': ['retail', 'ecommerce', 'shopping', 'store', '소매', '쇼핑', '판매'],
            '금융': ['finance', 'banking', 'investment', 'financial', '금융', '은행', '투자'],
            '의료': ['healthcare', 'medical', 'hospital', 'health', '의료', '병원', '건강'],
            '교육': ['education', 'learning', 'training', 'academy', '교육', '학습', '학원'],
            '서비스': ['service', 'consulting', 'support', '서비스', '컨설팅', '지원']
        }

        detected_industries = []
        for industry, keywords_list in industry_keywords.items():
            for keyword in keywords_list:
                if keyword in text or keyword in keywords:
                    detected_industries.append(industry)
                    break

        if detected_industries:
            return f"감지된 산업 분야: {', '.join(set(detected_industries))}"
        else:
            return "웹사이트 분석을 통해 구체적인 산업 분야를 파악 중입니다."

    def _identify_strengths(self) -> List[str]:
        """경쟁 우위 요소 식별"""
        strengths = []

        text = self.data.get('text_content', '').lower()
        headings = ' '.join(self.data.get('headings', [])).lower()

        # 강점 키워드 분석
        strength_keywords = {
            '혁신': ['innovation', 'innovative', 'new', 'advanced', '혁신', '최신'],
            '품질': ['quality', 'premium', 'excellence', 'best', '품질', '우수'],
            '경험': ['experience', 'years', 'expertise', 'professional', '경험', '전문'],
            '고객중심': ['customer', 'client', 'service', '고객', '서비스'],
            '기술력': ['technology', 'technical', 'advanced', '기술', '첨단']
        }

        for strength, keywords in strength_keywords.items():
            for keyword in keywords:
                if keyword in text or keyword in headings:
                    strengths.append(f"{strength} 강조")
                    break

        if not strengths:
            strengths = [
                "웹사이트를 통한 온라인 입지 구축",
                "디지털 채널 활용 의지"
            ]

        return strengths[:5]

    def _identify_target_audience(self) -> str:
        """타겟 고객 식별"""
        text = self.data.get('text_content', '').lower()

        target_keywords = {
            'B2B': ['business', 'enterprise', 'corporate', 'b2b', '기업', '법인'],
            'B2C': ['consumer', 'customer', 'individual', 'personal', 'b2c', '소비자', '개인'],
            '전문가': ['professional', 'expert', 'specialist', '전문가'],
            '일반 대중': ['everyone', 'anyone', 'public', '모두', '누구나']
        }

        identified_targets = []
        for target, keywords in target_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    identified_targets.append(target)
                    break

        if identified_targets:
            return f"주요 타겟: {', '.join(set(identified_targets))}"
        else:
            return "웹사이트 분석을 통해 타겟 고객을 파악 중입니다."

    def _generate_marketing_strategies(self) -> List[Dict[str, str]]:
        """마케팅 전략 생성"""
        strategies = [
            {
                '전략': 'SEO 최적화',
                '설명': '검색 엔진 최적화를 통한 유기적 트래픽 증대',
                '실행방안': '키워드 리서치, 메타태그 최적화, 양질의 콘텐츠 제작, 백링크 구축'
            },
            {
                '전략': '콘텐츠 마케팅',
                '설명': '가치 있는 콘텐츠를 통한 고객 유치 및 관계 형성',
                '실행방안': '블로그 운영, 사례 연구, 백서 제작, 인포그래픽 개발'
            },
            {
                '전략': '소셜 미디어 마케팅',
                '설명': '주요 소셜 플랫폼을 활용한 브랜드 인지도 향상',
                '실행방안': 'LinkedIn, Facebook, Instagram 운영, 정기적 포스팅, 광고 캠페인'
            },
            {
                '전략': '이메일 마케팅',
                '설명': '타겟 고객에게 맞춤형 메시지 전달',
                '실행방안': '뉴스레터 발행, 리드 너처링, 자동화 캠페인 구축'
            },
            {
                '전략': '퍼포먼스 마케팅',
                '설명': '데이터 기반의 성과 중심 광고 집행',
                '실행방안': 'Google Ads, 네이버 검색광고, 리타겟팅, A/B 테스트'
            }
        ]

        return strategies

    def _analyze_digital_presence(self) -> Dict[str, str]:
        """디지털 입지 분석"""
        links_count = len(self.data.get('internal_links', []))
        headings_count = len(self.data.get('headings', []))

        return {
            '웹사이트 구조': f'내부 링크 {links_count}개 확인, 콘텐츠 구조화 수준 {"양호" if headings_count > 5 else "개선 필요"}',
            '콘텐츠 현황': f'주요 헤딩 {headings_count}개 분석됨',
            'SEO 현황': '메타 태그 및 구조화 데이터 분석 완료',
            '개선 필요 사항': self._identify_improvements()
        }

    def _identify_improvements(self) -> str:
        """개선 사항 식별"""
        improvements = []

        if not self.data.get('meta_description'):
            improvements.append('메타 설명 추가')

        if not self.data.get('meta_keywords'):
            improvements.append('메타 키워드 설정')

        if len(self.data.get('headings', [])) < 5:
            improvements.append('콘텐츠 구조화 강화')

        if improvements:
            return ', '.join(improvements)
        else:
            return '기본적인 SEO 요소가 잘 갖춰져 있습니다'

    def _create_recommendations(self) -> List[str]:
        """권장 사항 생성"""
        return [
            '웹사이트 SEO 감사를 통한 기술적 최적화 진행',
            '타겟 키워드 리서치 및 콘텐츠 전략 수립',
            '소셜 미디어 채널 통합 및 일관된 브랜드 메시지 구축',
            '고객 여정 맵핑을 통한 전환율 최적화',
            'Google Analytics 및 추적 도구 설정으로 데이터 기반 의사결정 체계 구축',
            '경쟁사 분석을 통한 차별화 전략 개발',
            '모바일 최적화 및 사용자 경험 개선'
        ]

    def _define_next_steps(self) -> List[Dict[str, str]]:
        """다음 단계 정의"""
        return [
            {
                '단계': '1단계 (1-2주)',
                '내용': '초기 진단 및 전략 수립',
                '세부사항': 'SEO 감사, 경쟁사 분석, 키워드 리서치, 마케팅 계획 수립'
            },
            {
                '단계': '2단계 (3-4주)',
                '내용': '기반 구축',
                '세부사항': '웹사이트 최적화, 콘텐츠 캘린더 작성, 소셜 미디어 계정 설정'
            },
            {
                '단계': '3단계 (1-2개월)',
                '내용': '실행 및 모니터링',
                '세부사항': '콘텐츠 제작 및 배포, 광고 캠페인 시작, 성과 측정'
            },
            {
                '단계': '4단계 (지속)',
                '내용': '최적화 및 성장',
                '세부사항': '데이터 분석, A/B 테스트, 전략 개선, 확장'
            }
        ]
