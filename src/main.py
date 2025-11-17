"""
마케팅 제안서 자동화 메인 스크립트
"""

import os
import sys
from datetime import datetime
from web_scraper import WebScraper
from analyzer import BusinessAnalyzer
from docx_generator import ProposalGenerator
from notion_generator import NotionGenerator


def create_proposal(company_name: str, url: str, output_dir: str = '../output',
                    use_notion: bool = False, notion_token: str = None,
                    parent_page_id: str = None) -> dict:
    """
    마케팅 제안서 생성

    Args:
        company_name: 기업명
        url: 기업 웹사이트 URL
        output_dir: 출력 디렉토리
        use_notion: Notion 출력 여부
        notion_token: Notion API 토큰
        parent_page_id: Notion 부모 페이지 ID

    Returns:
        생성된 파일 정보 딕셔너리
    """
    print(f"\n{'='*60}")
    print(f"기업 분석 및 마케팅 전략 보고서 자동화 시스템")
    print(f"{'='*60}\n")

    # 1단계: 웹 스크래핑
    print(f"[1/5] 웹사이트 스크래핑 중...")
    print(f"      대상: {url}")
    scraper = WebScraper(url)
    scraped_data = scraper.scrape_website()

    if scraped_data.get('status') == 'error':
        print(f"      ⚠ 경고: {scraped_data.get('error_message')}")
        print(f"      기본 템플릿으로 제안서를 생성합니다.\n")
    else:
        print(f"      ✓ 스크래핑 완료\n")

    # 2단계: 분석
    print(f"[2/5] 기업 분석 및 전략 수립 중...")
    analyzer = BusinessAnalyzer(company_name, scraped_data)
    analysis = analyzer.analyze()
    print(f"      ✓ 분석 완료\n")

    results = {}

    # 3단계: DOCX 문서 생성
    print(f"[3/5] DOCX 보고서 생성 중...")
    generator = ProposalGenerator(analysis)

    # 출력 디렉토리 확인 및 생성
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)

    # 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_company_name = "".join(
        c for c in company_name if c.isalnum() or c in (' ', '_', '-')
    ).strip()
    filename = f"기업분석보고서_{safe_company_name}_{timestamp}.docx"
    file_path = os.path.join(output_path, filename)

    # 문서 생성
    generator.generate(file_path)
    print(f"      ✓ DOCX 생성 완료\n")

    results['docx_path'] = file_path
    results['docx_size'] = os.path.getsize(file_path) / 1024

    # 4단계: Notion 페이지 생성 (옵션)
    print(f"[4/5] Notion 페이지 생성 중...")
    if use_notion:
        notion_gen = NotionGenerator(
            analysis,
            notion_token=notion_token,
            parent_page_id=parent_page_id
        )
        notion_result = notion_gen.generate()
        print(f"      {notion_result}\n")
        results['notion_result'] = notion_result
    else:
        print(f"      ⊘ Notion 출력 비활성화 (활성화하려면 --notion 옵션 사용)\n")
        results['notion_result'] = '비활성화'

    # 5단계: 완료
    print(f"[5/5] 완료!")
    print(f"\n{'='*60}")
    print(f"보고서가 성공적으로 생성되었습니다!")
    print(f"{'='*60}")
    print(f"\n📄 DOCX 파일 위치: {file_path}")
    print(f"   파일 크기: {results['docx_size']:.2f} KB")

    if use_notion and 'notion_result' in results:
        print(f"\n🌐 Notion: {results['notion_result']}")

    print()

    return results


def main():
    """메인 함수"""
    print("\n기업 분석 및 마케팅 전략 보고서 자동화 시스템에 오신 것을 환영합니다!\n")

    # 커맨드라인 인자 파싱
    use_notion = '--notion' in sys.argv
    if use_notion:
        sys.argv.remove('--notion')

    # 사용자 입력
    if len(sys.argv) >= 3:
        # 커맨드라인 인자 사용
        company_name = sys.argv[1]
        url = sys.argv[2]
    else:
        # 대화형 입력
        company_name = input("기업명을 입력하세요: ").strip()
        if not company_name:
            print("기업명을 입력해야 합니다.")
            return

        url = input("기업 웹사이트 URL을 입력하세요: ").strip()
        if not url:
            print("URL을 입력해야 합니다.")
            return

        # Notion 사용 여부 확인
        notion_input = input("Notion으로도 출력하시겠습니까? (y/N): ").strip().lower()
        use_notion = notion_input == 'y'

        # URL 프로토콜 확인
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

    # Notion 설정 확인
    notion_token = None
    parent_page_id = None

    if use_notion:
        notion_token = os.getenv('NOTION_TOKEN')
        parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')

        if not notion_token or not parent_page_id:
            print("\n⚠️  Notion 설정이 필요합니다:")
            print("   1. NOTION_TOKEN 환경변수 설정")
            print("   2. NOTION_PARENT_PAGE_ID 환경변수 설정")
            print("\n   설정 방법:")
            print("   export NOTION_TOKEN='your_token_here'")
            print("   export NOTION_PARENT_PAGE_ID='your_page_id_here'")
            print("\n   DOCX 파일만 생성합니다...\n")
            use_notion = False

    try:
        results = create_proposal(
            company_name,
            url,
            use_notion=use_notion,
            notion_token=notion_token,
            parent_page_id=parent_page_id
        )
        print(f"프로세스가 성공적으로 완료되었습니다!\n")
        return results

    except Exception as e:
        print(f"\n오류 발생: {str(e)}")
        print(f"자세한 내용은 로그를 확인해주세요.\n")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
