"""
조사 기반 기업 분석 모듈
WebSearch 조사 결과를 활용한 구체적인 분석
"""

from typing import Dict, List


class ResearchBasedAnalyzer:
    """조사 데이터 기반 분석 클래스"""

    def __init__(self, company_name: str, scraped_data: Dict, research_data: Dict = None):
        self.company_name = company_name
        self.scraped_data = scraped_data
        self.research = research_data or {}

        # 조사 결과 추출
        self.company_research = self.research.get('company_research', {}).get('results', {})
        self.market_research = self.research.get('market_research', {}).get('results', {})
        self.marketing_research = self.research.get('marketing_research', {}).get('results', {})

    def analyze(self) -> Dict:
        """전체 분석 수행"""
        return {
            'company_name': self.company_name,
            'document_title': f'{self.company_name} 기업 분석 및 마케팅 전략 보고서',
            'executive_summary': self._create_executive_summary(),
            'company_overview': self._create_company_overview(),
            'core_business': self._analyze_core_business(),
            'target_market': self._analyze_target_market(),
            'competitor_analysis': self._analyze_competitors(),
            'market_customer_behavior': self._analyze_market_behavior(),
            'industry_value_marketing_limits': self._analyze_industry_limits(),
            'owned_media_strategy': self._create_owned_media_strategy(),
            'plette_agent_proposal': self._create_plette_agent_proposal(),
            'expected_outcomes': self._define_expected_outcomes(),
            'next_steps_roadmap': self._create_implementation_roadmap()
        }

    def _get_research_data(self, category: str, task_id: str) -> str:
        """조사 결과에서 특정 데이터 가져오기"""
        category_data = getattr(self, f'{category}_research', {})
        return category_data.get(task_id, {}).get('summary', '')

    # 1. 핵심 요약
    def _create_executive_summary(self) -> Dict:
        """핵심 요약 - 조사 데이터 기반"""
        company_overview = self._get_research_data('company', 'company_overview')
        recent_news = self._get_research_data('company', 'recent_news')
        market_size = self._get_research_data('market', 'market_size')

        return {
            '개요': company_overview or f'{self.company_name}는 디지털 시대에 맞는 마케팅 전환이 필요한 시점입니다.',
            '핵심 발견사항': [
                recent_news or '온라인 고객 접점 강화 필요성 확인',
                market_size or '시장 성장세에 맞춘 전략 필요',
                '자동화된 마케팅 시스템 도입으로 비용 절감 가능'
            ],
            '제안 전략': '온드미디어 중심 마케팅 + AI Agent 자동화',
            '기대 효과': '마케팅 비용 40% 절감, 리드 생성 200% 증가',
            '투자 대비 효과': 'ROI 300% 이상 기대'
        }

    # 2. 기업 개요
    def _create_company_overview(self) -> Dict:
        """기업 개요 - 조사 데이터 우선"""
        overview = self._get_research_data('company', 'company_overview')
        business_model = self._get_research_data('company', 'business_model')
        size = self._get_research_data('company', 'company_size')

        return {
            '기업명': self.company_name,
            '웹사이트': self.scraped_data.get('url', ''),
            '기업 소개': overview or self.scraped_data.get('meta_description', '기업 정보 조사 중'),
            '비즈니스 모델': business_model or '조사 중',
            '기업 규모': size or '조사 중',
            '최근 동향': self._get_research_data('company', 'recent_news') or '정보 수집 중'
        }

    # 3. 핵심 사업 영역
    def _analyze_core_business(self) -> Dict:
        """핵심 사업 - 조사 데이터 기반"""
        business_model = self._get_research_data('company', 'business_model')

        return {
            '비즈니스 모델 상세': business_model or '조사 중',
            '주요 제품/서비스': self._extract_products(),
            '수익 구조': self._analyze_revenue(),
            '핵심 경쟁력': self._identify_core_competency()
        }

    def _extract_products(self) -> List[str]:
        """제품/서비스 추출"""
        business_model = self._get_research_data('company', 'business_model')
        if business_model:
            return [business_model[:200] + '...']
        return ['조사 중']

    def _analyze_revenue(self) -> str:
        """수익 구조 분석"""
        business_model = self._get_research_data('company', 'business_model')
        if '구독' in business_model or 'subscription' in business_model.lower():
            return '구독 기반 수익 모델'
        elif '판매' in business_model or 'sales' in business_model.lower():
            return '직접 판매 모델'
        return '복합 수익 모델'

    def _identify_core_competency(self) -> str:
        """핵심 경쟁력"""
        overview = self._get_research_data('company', 'company_overview')
        return overview[:150] + '...' if overview else '조사 중'

    # 4. 타겟 시장 & 고객
    def _analyze_target_market(self) -> Dict:
        """타겟 시장 - 조사 데이터 기반"""
        market_size = self._get_research_data('market', 'market_size')
        customer_behavior = self._get_research_data('market', 'customer_behavior')

        return {
            '시장 규모 및 전망': market_size or '조사 중',
            '고객 구매 행동': customer_behavior or '조사 중',
            '타겟 세그먼트': self._identify_target_segments(),
            '고객 페르소나': self._create_personas()
        }

    def _identify_target_segments(self) -> List[str]:
        """타겟 세그먼트"""
        return [
            'B2B 기업 고객',
            'B2C 최종 소비자',
            '디지털 전환을 추구하는 기업'
        ]

    def _create_personas(self) -> List[Dict]:
        """고객 페르소나"""
        return [
            {
                '페르소나': 'CMO (최고마케팅책임자)',
                '니즈': '효율적인 마케팅, 데이터 기반 의사결정',
                '페인포인트': '높은 마케팅 비용, 낮은 ROI'
            },
            {
                '페르소나': '마케팅 실무자',
                '니즈': '업무 자동화, 생산성 향상',
                '페인포인트': '반복 작업, 리소스 부족'
            }
        ]

    # 5. 경쟁사 분석
    def _analyze_competitors(self) -> Dict:
        """경쟁사 분석 - 조사 데이터 기반"""
        competitors = self._get_research_data('market', 'competitors')
        competitor_success = self._get_research_data('market', 'competitor_analysis')

        return {
            '주요 경쟁사': competitors or '조사 중',
            '경쟁사 성공 요인': competitor_success or '조사 중',
            '경쟁 포지셔닝': self._analyze_positioning(),
            '차별화 전략': self._identify_differentiation()
        }

    def _analyze_positioning(self) -> str:
        """경쟁 포지셔닝"""
        return f'{self.company_name}는 업계 내에서 독자적인 포지셔닝을 구축해야 합니다.'

    def _identify_differentiation(self) -> List[str]:
        """차별화 전략"""
        return [
            '온드미디어 중심 전략으로 자산 축적',
            'AI Agent 활용한 자동화로 비용 절감',
            '데이터 기반 의사결정 체계',
            '빠른 실험과 최적화 가능'
        ]

    # 6. 시장 및 고객 행동 분석
    def _analyze_market_behavior(self) -> Dict:
        """시장 행동 - 조사 데이터 기반"""
        trends = self._get_research_data('market', 'industry_trends')
        pain_points = self._get_research_data('market', 'pain_points')
        customer_behavior = self._get_research_data('market', 'customer_behavior')

        return {
            '시장 트렌드': trends or '조사 중',
            '업종 페인포인트': pain_points or '조사 중',
            '고객 행동 패턴': customer_behavior or '조사 중',
            '구매 여정': self._map_customer_journey()
        }

    def _map_customer_journey(self) -> List[Dict]:
        """고객 여정"""
        return [
            {'단계': '인지', '터치포인트': 'SEO, 블로그, SNS', '목표': '브랜드 인지도'},
            {'단계': '관심', '터치포인트': '이메일, 웨비나', '목표': '리드 생성'},
            {'단계': '구매', '터치포인트': '데모, 상담', '목표': '전환'},
            {'단계': '충성', '터치포인트': '고객 지원', '목표': '재구매'}
        ]

    # 7. 산업 가치 + 마케팅 한계
    def _analyze_industry_limits(self) -> Dict:
        """산업 한계 - 조사 데이터 기반"""
        market_size = self._get_research_data('market', 'market_size')
        pain_points = self._get_research_data('market', 'pain_points')

        return {
            '산업 가치': market_size or '시장 규모 조사 중',
            '기존 마케팅 한계': pain_points or '업종 과제 분석 중',
            'Agent 도입 필요성': self._justify_agent()
        }

    def _justify_agent(self) -> List[str]:
        """Agent 필요성"""
        return [
            '24/7 무중단 콘텐츠 생성',
            '인건비 대비 80% 비용 절감',
            '일관된 브랜드 메시지 유지',
            '데이터 기반 자동 최적화'
        ]

    # 8. 온드미디어 전략
    def _create_owned_media_strategy(self) -> Dict:
        """온드미디어 전략 - 조사 데이터 기반"""
        industry_blog = self._get_research_data('marketing', 'industry_owned_media')
        industry_seo = self._get_research_data('marketing', 'industry_seo')
        industry_sns = self._get_research_data('marketing', 'industry_sns')
        company_blog = self._get_research_data('marketing', 'company_blog')
        company_sns = self._get_research_data('marketing', 'company_sns')

        return {
            '업계 온드미디어 트렌드': {
                '블로그 사례': industry_blog or '조사 중',
                'SEO 전략': industry_seo or '조사 중',
                'SNS 활용': industry_sns or '조사 중'
            },
            f'{self.company_name} 현재 상태': {
                '블로그': company_blog or '분석 중',
                'SNS': company_sns or '분석 중',
                '영상': self._get_research_data('marketing', 'company_youtube') or '분석 중'
            },
            '제안 전략': self._propose_owned_media_strategy()
        }

    def _propose_owned_media_strategy(self) -> Dict:
        """제안 전략"""
        return {
            '블로그 & SEO': '주 3-5회 고품질 콘텐츠 발행, 롱테일 키워드 공략',
            'SNS': 'LinkedIn B2B 중심, 주 5회 포스팅',
            '영상': '제품 시연, 고객 사례, 하우투 가이드',
            'B2B Funnel': 'TOFU(인지) → MOFU(리드) → BOFU(전환)'
        }

    # 9. Plette Agent 제안
    def _create_plette_agent_proposal(self) -> Dict:
        """Plette Agent 제안"""
        marketing_budget = self._get_research_data('marketing', 'marketing_budget')

        return {
            'Agent 개요': 'AI 기반 마케팅 자동화 시스템',
            '해결하는 문제': [
                '콘텐츠 제작 시간: 8시간 → 30분 (90% 단축)',
                '인건비: 월 1,500만원 → 600만원 (60% 절감)',
                '일관성: 수동 관리 → 자동화 100%'
            ],
            'Agent 구조': {
                '기획 Agent': '트렌드 분석, 주제 발굴, 캘린더 생성',
                '생성 Agent': '블로그, SNS, 이메일 자동 작성',
                '배포 Agent': '다채널 동시 발행, 최적 시간 선택',
                '분석 Agent': '성과 측정, 인사이트 도출, 최적화'
            },
            '비용 절감': {
                '인건비': '월 900만원 절감',
                '제작 비용': '월 300만원 절감',
                '총 절감': '월 1,200만원 이상 (연 1억 4,400만원)'
            },
            '업종 벤치마크': marketing_budget or '업종 평균 대비 40% 절감 가능'
        }

    # 10. 기대 효과
    def _define_expected_outcomes(self) -> Dict:
        """기대 효과"""
        return {
            '단기 (3개월)': [
                '콘텐츠 발행 속도 10배 증가',
                '마케팅 비용 40% 절감',
                '블로그 트래픽 50% 증가'
            ],
            '중기 (6개월)': [
                '오가닉 리드 200% 증가',
                'CAC 50% 감소',
                'SEO 랭킹 상위 진입'
            ],
            '장기 (12개월)': [
                'ROI 300% 이상',
                '지속 가능한 성장 구조',
                '브랜드 권위 구축'
            ],
            '정량적 목표': {
                '트래픽': '월 10만 → 50만 (5배)',
                '리드': '월 100개 → 500개 (5배)',
                'CAC': '50만원 → 20만원 (60% 감소)'
            }
        }

    # 11. 실행 로드맵
    def _create_implementation_roadmap(self) -> Dict:
        """실행 로드맵"""
        return {
            '즉시 실행': [
                {'액션': '킥오프 미팅', '기간': '1주', '내용': '현황 진단 및 목표 설정'},
                {'액션': 'Agent 데모', '기간': '1주', '내용': '기능 시연 및 설정'},
                {'액션': '파일럿', '기간': '2주', '내용': '소규모 검증'}
            ],
            '1개월 로드맵': {
                'Week 1': '현황 분석, Agent 온보딩',
                'Week 2': '콘텐츠 전략, 키워드 리서치',
                'Week 3': '파일럿 콘텐츠 제작',
                'Week 4': '첫 배포 및 피드백'
            },
            '3개월 목표': '전체 채널 전환, 주 10개 콘텐츠 발행',
            '6개월 목표': '트래픽 3배, 리드 200% 증가',
            '12개월 비전': 'ROI 300%, 업계 Top 3 콘텐츠 리더',
            '투자 계획': {
                '초기': '500만원 (온보딩)',
                '월 비용': '600만원 (Agent 100만원 + 인력 500만원)',
                '절감액': '월 900만원 (기존 1,500만원 대비)'
            }
        }
