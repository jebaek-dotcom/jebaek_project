"""
기업 조사 코디네이터
웹 스크래핑으로 실제 자료를 조사합니다.
"""

from typing import Dict, List
import json


class ResearchCoordinator:
    """조사 항목을 정의하고 관리하는 클래스"""

    def __init__(self, company_name: str, url: str, homepage_data: Dict):
        self.company_name = company_name
        self.url = url
        self.homepage_data = homepage_data
        self.industry = self._detect_industry()

    def _detect_industry(self) -> str:
        """홈페이지 데이터에서 업종 감지"""
        text = self.homepage_data.get('text_content', '').lower()

        industry_keywords = {
            'IT/소프트웨어': ['software', 'saas', 'platform', 'app', 'cloud'],
            '이커머스': ['ecommerce', 'shopping', 'marketplace', 'retail'],
            '제조': ['manufacturing', 'factory', 'production'],
            '금융': ['finance', 'banking', 'fintech', 'payment'],
            '헬스케어': ['healthcare', 'medical', 'health'],
            '교육': ['education', 'learning', 'edtech'],
            '미디어': ['media', 'content', 'news'],
            '서비스': ['service', 'consulting', 'agency']
        }

        for industry, keywords in industry_keywords.items():
            if any(kw in text for kw in keywords):
                return industry

        return '종합'

    def generate_research_tasks(self) -> Dict:
        """조사 항목 생성"""

        tasks = {
            "company_name": self.company_name,
            "url": self.url,
            "industry": self.industry,
            "timestamp": None,  # Claude가 채울 것

            # 기업 분석
            "company_research": {
                "description": "기업에 대한 심층 조사",
                "tasks": [
                    {
                        "id": "company_overview",
                        "query": f"{self.company_name} 기업 개요 소개",
                        "description": "기업의 설립 연도, 비전, 미션, 주요 연혁"
                    },
                    {
                        "id": "recent_news",
                        "query": f"{self.company_name} 최근 3년 뉴스",
                        "description": "최근 3년간 주요 뉴스, 이벤트, 성과"
                    },
                    {
                        "id": "business_model",
                        "query": f"{self.company_name} 비즈니스 모델 수익구조",
                        "description": "어떻게 돈을 버는지, 주요 제품/서비스"
                    },
                    {
                        "id": "company_size",
                        "query": f"{self.company_name} 직원수 매출 규모",
                        "description": "기업 규모, 직원 수, 매출액"
                    },
                    {
                        "id": "customer_reviews",
                        "query": f"{self.company_name} 고객 리뷰 평가",
                        "description": "고객 평가, 리뷰, 만족도"
                    }
                ]
            },

            # 시장 분석
            "market_research": {
                "description": "업종 및 시장 조사",
                "tasks": [
                    {
                        "id": "market_size",
                        "query": f"{self.industry} 시장 규모 전망",
                        "description": "시장 규모, 성장률, 전망"
                    },
                    {
                        "id": "competitors",
                        "query": f"{self.industry} 주요 기업 경쟁사",
                        "description": "업종 내 상위 5개 기업, 시장 점유율"
                    },
                    {
                        "id": "competitor_analysis",
                        "query": f"{self.industry} 1위 기업 성공 요인",
                        "description": "업종 선두 기업의 성공 전략"
                    },
                    {
                        "id": "industry_trends",
                        "query": f"{self.industry} 최신 트렌드 2024",
                        "description": "최신 업종 트렌드, 기술 동향"
                    },
                    {
                        "id": "pain_points",
                        "query": f"{self.industry} 업종 문제점 과제",
                        "description": "업종의 공통 페인포인트, 해결 과제"
                    },
                    {
                        "id": "customer_behavior",
                        "query": f"{self.industry} 고객 구매 행동 패턴",
                        "description": "고객이 어떻게 의사결정하는지"
                    }
                ]
            },

            # 마케팅 분석
            "marketing_research": {
                "description": "온드미디어 및 마케팅 전략 조사",
                "tasks": [
                    {
                        "id": "industry_owned_media",
                        "query": f"{self.industry} 기업 블로그 마케팅 사례",
                        "description": "업종 기업들의 블로그 운영 사례"
                    },
                    {
                        "id": "industry_seo",
                        "query": f"{self.industry} SEO 콘텐츠 마케팅 전략",
                        "description": "업종의 SEO 및 콘텐츠 마케팅 전략"
                    },
                    {
                        "id": "industry_sns",
                        "query": f"{self.industry} SNS 소셜미디어 마케팅",
                        "description": "업종의 SNS 활용 사례"
                    },
                    {
                        "id": "company_blog",
                        "query": f"{self.company_name} 블로그 운영",
                        "description": f"{self.company_name}의 블로그 운영 현황"
                    },
                    {
                        "id": "company_sns",
                        "query": f"{self.company_name} SNS 인스타그램 페이스북",
                        "description": f"{self.company_name}의 SNS 채널 운영 현황"
                    },
                    {
                        "id": "company_youtube",
                        "query": f"{self.company_name} 유튜브 영상 마케팅",
                        "description": f"{self.company_name}의 영상 콘텐츠 마케팅"
                    },
                    {
                        "id": "marketing_budget",
                        "query": f"{self.industry} 마케팅 예산 배분 트렌드",
                        "description": "업종의 마케팅 예산 사용 패턴"
                    }
                ]
            }
        }

        return tasks

    def save_tasks(self, filename: str = 'research_tasks.json'):
        """조사 항목을 JSON 파일로 저장"""
        tasks = self.generate_research_tasks()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

        return filename

    def print_task_summary(self, tasks: Dict):
        """조사 항목 요약 출력"""
        print("\n" + "="*60)
        print("📋 조사 항목 생성 완료")
        print("="*60)
        print(f"\n기업명: {tasks['company_name']}")
        print(f"업종: {tasks['industry']}")
        print(f"\n총 조사 항목: {self._count_tasks(tasks)}개\n")

        print("📊 [1] 기업 분석 (Company Research)")
        for task in tasks['company_research']['tasks']:
            print(f"  - {task['description']}")

        print("\n📈 [2] 시장 분석 (Market Research)")
        for task in tasks['market_research']['tasks']:
            print(f"  - {task['description']}")

        print("\n📢 [3] 마케팅 조사 (Marketing Research)")
        for task in tasks['marketing_research']['tasks']:
            print(f"  - {task['description']}")

        print("\n" + "="*60)

    def _count_tasks(self, tasks: Dict) -> int:
        """전체 조사 항목 개수 세기"""
        count = 0
        count += len(tasks.get('company_research', {}).get('tasks', []))
        count += len(tasks.get('market_research', {}).get('tasks', []))
        count += len(tasks.get('marketing_research', {}).get('tasks', []))
        return count


def load_research_results(filename: str = 'research_results.json') -> Dict:
    """조사 결과 로드"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def validate_research_results(results: Dict) -> bool:
    """조사 결과 유효성 검증"""
    if not results:
        return False

    required_sections = ['company_research', 'market_research', 'marketing_research']

    for section in required_sections:
        if section not in results:
            return False
        if 'results' not in results[section]:
            return False

    return True
