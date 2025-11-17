"""
Notion 연결 테스트 스크립트
"""
import os
from notion_client import Client

# 환경변수에서 가져오기
notion_token = os.getenv('NOTION_TOKEN')
page_id = os.getenv('NOTION_PARENT_PAGE_ID')

print("Notion API 연결 테스트 시작...\n")
print(f"Token: {notion_token[:20]}...")
print(f"Page ID: {page_id}\n")

try:
    notion = Client(auth=notion_token)

    # 페이지 정보 조회 시도
    print("1. 페이지 정보 조회 중...")
    page = notion.pages.retrieve(page_id=page_id)
    print(f"   ✓ 페이지 조회 성공!")
    print(f"   페이지 제목: {page.get('properties', {})}\n")

    # 간단한 페이지 생성 테스트
    print("2. 테스트 페이지 생성 시도...")
    test_page = notion.pages.create(
        parent={"page_id": page_id},
        properties={
            "title": {
                "title": [{"text": {"content": "연결 테스트"}}]
            }
        }
    )
    print(f"   ✓ 페이지 생성 성공!")
    print(f"   URL: {test_page.get('url')}\n")

except Exception as e:
    print(f"   ✗ 오류 발생: {str(e)}\n")
    print(f"   오류 타입: {type(e).__name__}")

    # 더 자세한 에러 정보
    if hasattr(e, 'status'):
        print(f"   HTTP 상태: {e.status}")
    if hasattr(e, 'body'):
        print(f"   응답 내용: {e.body}")
