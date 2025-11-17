"""
마케팅 제안서 자동화 메인 스크립트 (DOCX 전용)
"""

import os
import sys
from datetime import datetime
from web_scraper import WebScraper
from analyzer import BusinessAnalyzer
from docx_generator import ProposalGenerator


def create_proposal(company_name: str, url: str, output_dir: str = '../output') -> dict:
    """
    마케팅 제안서 생성 (DOCX 전용)

    Args:
        company_name: 기업명
        url: 기업 웹사이트 URL
        output_dir: 출력 디렉토리

    Returns:
        생성된 파일 정보 딕셔너리
    """
    print(f"\n{'='*60}")
    print(f"기업 분석 및 마케팅 전략 보고서 자동화 시스템")
    print(f"{'='*60}\n")

    # 1단계: 웹 스크래핑
    print(f"[1/4] 웹사이트 스크래핑 중...")
    print(f"      대상: {url}")
    scraper = WebScraper(url)
    scraped_data = scraper.scrape_website()

    if scraped_data.get('status') == 'error':
        print(f"      ⚠ 경고: {scraped_data.get('error_message')}")
        print(f"      기본 템플릿으로 제안서를 생성합니다.\n")
    else:
        print(f"      ✓ 스크래핑 완료\n")

    # 2단계: 분석
    print(f"[2/4] 기업 분석 및 전략 수립 중...")
    analyzer = BusinessAnalyzer(company_name, scraped_data)
    analysis = analyzer.analyze()
    print(f"      ✓ 분석 완료\n")

    results = {}

    # 3단계: DOCX 문서 생성
    print(f"[3/4] DOCX 보고서 생성 중...")
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

    # 4단계: 완료
    print(f"[4/4] 완료!")
    print(f"\n{'='*60}")
    print(f"보고서가 성공적으로 생성되었습니다!")
    print(f"{'='*60}")
    print(f"\n📄 DOCX 파일 위치: {file_path}")
    print(f"   파일 크기: {results['docx_size']:.2f} KB")
    print()

    return results


def main():
    """메인 함수"""
    print("\n기업 분석 및 마케팅 전략 보고서 자동화 시스템에 오신 것을 환영합니다!\n")

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

    # URL 프로토콜 확인
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        results = create_proposal(company_name, url)
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
