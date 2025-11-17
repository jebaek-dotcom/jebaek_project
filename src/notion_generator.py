"""
Notion 페이지 생성 모듈
Notion API를 사용하여 보고서를 Notion 페이지로 생성합니다.
"""

from typing import Dict, List
import os


class NotionGenerator:
    def __init__(self, analysis_data: Dict, notion_token: str = None, parent_page_id: str = None):
        """
        Notion Generator 초기화

        Args:
            analysis_data: 분석 데이터
            notion_token: Notion API 토큰 (환경변수 NOTION_TOKEN에서도 가져올 수 있음)
            parent_page_id: 부모 페이지 ID (환경변수 NOTION_PARENT_PAGE_ID에서도 가져올 수 있음)
        """
        self.data = analysis_data
        self.notion_token = notion_token or os.getenv('NOTION_TOKEN')
        self.parent_page_id = parent_page_id or os.getenv('NOTION_PARENT_PAGE_ID')

        # Notion 클라이언트 초기화
        if self.notion_token:
            try:
                from notion_client import Client
                self.notion = Client(auth=self.notion_token)
            except ImportError:
                raise ImportError(
                    "notion-client가 설치되지 않았습니다. "
                    "'pip install notion-client'를 실행하세요."
                )
        else:
            self.notion = None

    def generate(self) -> str:
        """
        Notion 페이지 생성

        Returns:
            생성된 Notion 페이지 URL
        """
        if not self.notion:
            return "Notion API 토큰이 설정되지 않았습니다. 환경변수 NOTION_TOKEN을 설정하세요."

        if not self.parent_page_id:
            return "Notion 부모 페이지 ID가 설정되지 않았습니다. 환경변수 NOTION_PARENT_PAGE_ID를 설정하세요."

        try:
            # 페이지 생성
            page = self._create_page()
            return f"✓ Notion 페이지 생성 완료: {page['url']}"

        except Exception as e:
            return f"Notion 페이지 생성 실패: {str(e)}"

    def _create_page(self) -> Dict:
        """Notion 페이지 생성"""
        company_name = self.data.get('company_name', '기업명')
        doc_title = self.data.get('document_title', '기업 분석 및 마케팅 전략 보고서')

        # 페이지 생성
        page = self.notion.pages.create(
            parent={"page_id": self.parent_page_id},
            properties={
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": f"{company_name} - {doc_title}"
                            }
                        }
                    ]
                }
            },
            children=self._build_page_content()
        )

        return page

    def _build_page_content(self) -> List[Dict]:
        """페이지 콘텐츠 블록 생성"""
        blocks = []

        # 표지 정보
        blocks.extend(self._cover_section())

        # 목차
        blocks.extend(self._toc_section())

        # 1. 핵심 요약
        blocks.extend(self._executive_summary_section())

        # 2. 기업 개요
        blocks.extend(self._company_overview_section())

        # 3. 핵심 사업 영역
        blocks.extend(self._core_business_section())

        # 4. 타겟 시장
        blocks.extend(self._target_market_section())

        # 5. 경쟁사 분석
        blocks.extend(self._competitor_analysis_section())

        # 6. 시장 및 고객 행동
        blocks.extend(self._market_behavior_section())

        # 7. 산업 가치 + 마케팅 한계
        blocks.extend(self._industry_limits_section())

        # 8. 온드미디어 전략
        blocks.extend(self._owned_media_strategy_section())

        # 9. Plette Agent 제안
        blocks.extend(self._plette_agent_section())

        # 10. 기대 효과
        blocks.extend(self._expected_outcomes_section())

        # 11. Next Steps
        blocks.extend(self._implementation_roadmap_section())

        return blocks

    def _cover_section(self) -> List[Dict]:
        """표지 섹션"""
        return [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"{self.data.get('document_title', '기업 분석 및 마케팅 전략 보고서')}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"{self.data.get('company_name', '기업명')}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"작성일: {self.data.get('created_date', '2024')}"}
                    }]
                }
            },
            {"object": "block", "type": "divider", "divider": {}}
        ]

    def _toc_section(self) -> List[Dict]:
        """목차 섹션"""
        return [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "목차"}}]
                }
            },
            {
                "object": "block",
                "type": "table_of_contents",
                "table_of_contents": {}
            },
            {"object": "block", "type": "divider", "divider": {}}
        ]

    def _executive_summary_section(self) -> List[Dict]:
        """1. 핵심 요약"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "1. 핵심 요약 (Executive Summary)"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "⚡ 의사결정권자를 위한 핵심 정리"}
                    }],
                    "icon": {"emoji": "⚡"}
                }
            }
        ]

        summary = self.data.get('executive_summary', {})
        for key, value in summary.items():
            if isinstance(value, list):
                blocks.append(self._heading_3(key))
                for item in value:
                    blocks.append(self._bullet_item(item))
            else:
                blocks.append(self._paragraph_bold(key, str(value)))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _company_overview_section(self) -> List[Dict]:
        """2. 기업 개요"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "2. 기업 개요"}}]
                }
            }
        ]

        overview = self.data.get('company_overview', {})
        for key, value in overview.items():
            blocks.append(self._paragraph_bold(key, str(value)))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _core_business_section(self) -> List[Dict]:
        """3. 핵심 사업 영역"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "3. 핵심 사업 영역"}}]
                }
            }
        ]

        core_business = self.data.get('core_business', {})
        for key, value in core_business.items():
            blocks.append(self._heading_2(key))

            if isinstance(value, list):
                for item in value:
                    blocks.append(self._bullet_item(item))
            else:
                blocks.append(self._paragraph(str(value)))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _target_market_section(self) -> List[Dict]:
        """4. 타겟 시장"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "4. 현재 타겟 시장 & 고객"}}]
                }
            }
        ]

        target = self.data.get('target_market', {})
        for key, value in target.items():
            blocks.append(self._heading_2(key))

            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    for item in value:
                        for k, v in item.items():
                            blocks.append(self._paragraph_bold(k, str(v)))
                else:
                    for item in value:
                        blocks.append(self._bullet_item(item))
            else:
                blocks.append(self._paragraph(str(value)))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _competitor_analysis_section(self) -> List[Dict]:
        """5. 경쟁사 분석"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "5. 경쟁사 분석"}}]
                }
            }
        ]

        competitor = self.data.get('competitor_analysis', {})
        for key, value in competitor.items():
            blocks.append(self._heading_2(key))

            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    for item in value:
                        for k, v in item.items():
                            blocks.append(self._paragraph_bold(k, str(v)))
                else:
                    for item in value:
                        blocks.append(self._bullet_item(item))
            else:
                blocks.append(self._paragraph(str(value)))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _market_behavior_section(self) -> List[Dict]:
        """6. 시장 및 고객 행동"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "6. 시장 및 고객 행동 분석"}}]
                }
            }
        ]

        behavior = self.data.get('market_customer_behavior', {})
        blocks.extend(self._process_nested_dict(behavior))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _industry_limits_section(self) -> List[Dict]:
        """7. 산업 가치 + 마케팅 한계"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "7. 산업·업계 가치 + 기존 마케팅의 한계"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "왜 새로운 전략과 Agent가 필요한가 (기업의 문제 정의 파트)"}
                    }],
                    "icon": {"emoji": "🔥"}
                }
            }
        ]

        limits = self.data.get('industry_value_marketing_limits', {})
        blocks.extend(self._process_nested_dict(limits))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _owned_media_strategy_section(self) -> List[Dict]:
        """8. 온드미디어 전략"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "8. 온드미디어 중심 마케팅 전략 제안"}}]
                }
            }
        ]

        strategy = self.data.get('owned_media_strategy', {})
        blocks.extend(self._process_nested_dict(strategy))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _plette_agent_section(self) -> List[Dict]:
        """9. Plette Agent 제안"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "9. Plette Agent 활용 제안"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "AI Agent 기반 마케팅 자동화 솔루션"}
                    }],
                    "icon": {"emoji": "🤖"}
                }
            }
        ]

        agent = self.data.get('plette_agent_proposal', {})
        blocks.extend(self._process_nested_dict(agent))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _expected_outcomes_section(self) -> List[Dict]:
        """10. 기대 효과"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "10. 기대 효과 및 결론"}}]
                }
            }
        ]

        outcomes = self.data.get('expected_outcomes', {})
        blocks.extend(self._process_nested_dict(outcomes))

        blocks.append({"object": "block", "type": "divider", "divider": {}})
        return blocks

    def _implementation_roadmap_section(self) -> List[Dict]:
        """11. Next Steps"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "11. Next Step 제안 및 도입 로드맵"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "실행 로드맵 및 투자 계획"}
                    }],
                    "icon": {"emoji": "🚀"}
                }
            }
        ]

        roadmap = self.data.get('next_steps_roadmap', {})
        blocks.extend(self._process_nested_dict(roadmap))

        return blocks

    # 헬퍼 메서드들
    def _process_nested_dict(self, data: Dict) -> List[Dict]:
        """중첩된 딕셔너리 처리"""
        blocks = []

        for key, value in data.items():
            blocks.append(self._heading_2(key))

            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    for item in value:
                        for k, v in item.items():
                            if isinstance(v, list):
                                blocks.append(self._paragraph_bold(k, ""))
                                for sub_item in v:
                                    blocks.append(self._bullet_item(sub_item))
                            else:
                                blocks.append(self._paragraph_bold(k, str(v)))
                else:
                    for item in value:
                        blocks.append(self._bullet_item(item))
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list):
                        blocks.append(self._paragraph_bold(k, ""))
                        for sub_item in v:
                            blocks.append(self._bullet_item(sub_item))
                    else:
                        blocks.append(self._paragraph_bold(k, str(v)))
            else:
                blocks.append(self._paragraph(str(value)))

        return blocks

    def _heading_2(self, text: str) -> Dict:
        """Heading 2 블록"""
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    def _heading_3(self, text: str) -> Dict:
        """Heading 3 블록"""
        return {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    def _paragraph(self, text: str) -> Dict:
        """일반 문단 블록"""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]  # Notion 제한
            }
        }

    def _paragraph_bold(self, key: str, value: str) -> Dict:
        """볼드 키 + 값 문단"""
        rich_text = [
            {"type": "text", "text": {"content": f"{key}: "}, "annotations": {"bold": True}}
        ]

        if value:
            rich_text.append({"type": "text", "text": {"content": value[:1900]}})

        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text}
        }

    def _bullet_item(self, text: str) -> Dict:
        """불릿 리스트 아이템"""
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }
