"""
마케팅 제안서 자동화 메인 스크립트 (조사 기반 버전)

워크플로우:
1. python main_research.py "회사명" "URL" --prepare
   → research_tasks.json 생성

2. Claude에게 조사 요청
   → research_results.json 생성

3. python main_research.py "회사명" "URL" --generate
   → DOCX 보고서 생성
"""

import os
import sys
from datetime import datetime
from web_scraper import WebScraper
from research_coordinator import ResearchCoordinator, load_research_results, validate_research_results
from analyzer_research import ResearchBasedAnalyzer
from docx_generator import ProposalGenerator


def prepare_research(company_name: str, url: str) -> dict:
    """
    1단계: 조사 준비
    홈페이지 스크래핑하고 조사 항목을 생성합니다.
    """
    print(f"\n{'='*60}")
    print(f"📋 STEP 1: 조사 준비")
    print(f"{'='*60}\n")

    # 홈페이지 스크래핑
    print(f"[1/2] 홈페이지 스크래핑 중...")
    print(f"      대상: {url}")
    scraper = WebScraper(url)
    homepage_data = scraper.scrape_website()

    if homepage_data.get('status') == 'error':
        print(f"      ⚠ 경고: {homepage_data.get('error_message')}")
        print(f"      기본 정보로 진행합니다.\n")
    else:
        print(f"      ✓ 스크래핑 완료\n")

    # 조사 항목 생성
    print(f"[2/2] 조사 항목 생성 중...")
    coordinator = ResearchCoordinator(company_name, url, homepage_data)
    tasks = coordinator.generate_research_tasks()

    # 파일 저장
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tasks_file = os.path.join(script_dir, 'research_tasks.json')
    coordinator.save_tasks(tasks_file)

    print(f"      ✓ 생성 완료\n")

    # 요약 출력
    coordinator.print_task_summary(tasks)

    # 다음 단계 안내
    print("\n" + "="*60)
    print("✅ 조사 준비 완료!")
    print("="*60)
    print(f"\n📁 파일 저장: {tasks_file}\n")
    print("🔍 다음 단계: Claude에게 조사 요청")
    print("-" * 60)
    print("Claude Code에서 다음과 같이 요청하세요:")
    print()
    print('  "research_tasks.json 파일을 읽고,')
    print('   각 조사 항목(tasks)에 대해 WebSearch로 검색해서')
    print('   결과를 research_results.json에 저장해줘."')
    print()
    print("-" * 60)
    print("\n💡 팁: Claude가 조사를 완료하면")
    print(f'    python main_research.py "{company_name}" "{url}" --generate')
    print("    를 실행하세요!\n")

    return {
        'status': 'prepared',
        'tasks_file': tasks_file,
        'task_count': coordinator._count_tasks(tasks)
    }


def generate_report(company_name: str, url: str, output_dir: str = '../output') -> dict:
    """
    3단계: 보고서 생성
    조사 결과를 바탕으로 상세한 보고서를 생성합니다.
    """
    print(f"\n{'='*60}")
    print(f"📄 STEP 3: 보고서 생성")
    print(f"{'='*60}\n")

    # 조사 결과 로드
    print(f"[1/4] 조사 결과 로드 중...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_file = os.path.join(script_dir, 'research_results.json')

    research_results = load_research_results(results_file)

    if not research_results:
        print(f"      ❌ 오류: research_results.json 파일을 찾을 수 없습니다.")
        print(f"\n      먼저 Claude에게 조사를 요청하세요!")
        print(f"      (--prepare 단계 참고)\n")
        return {'status': 'error', 'message': 'No research results'}

    if not validate_research_results(research_results):
        print(f"      ❌ 오류: 조사 결과가 완전하지 않습니다.")
        print(f"      Claude가 모든 항목을 조사했는지 확인하세요.\n")
        return {'status': 'error', 'message': 'Incomplete research'}

    print(f"      ✓ 조사 결과 로드 완료\n")

    # 홈페이지 데이터도 함께 로드 (기본 정보용)
    print(f"[2/4] 기본 데이터 수집 중...")
    scraper = WebScraper(url)
    homepage_data = scraper.scrape_website()
    print(f"      ✓ 완료\n")

    # 분석 (조사 결과 활용)
    print(f"[3/4] 심층 분석 중...")
    print(f"      조사 데이터를 기반으로 전략 수립 중...")
    analyzer = ResearchBasedAnalyzer(company_name, homepage_data, research_results)
    analysis = analyzer.analyze()
    print(f"      ✓ 분석 완료\n")

    # DOCX 생성
    print(f"[4/4] DOCX 보고서 생성 중...")
    generator = ProposalGenerator(analysis)

    # 출력 경로
    output_path = os.path.join(script_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)

    # 파일명
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_company_name = "".join(
        c for c in company_name if c.isalnum() or c in (' ', '_', '-')
    ).strip()
    filename = f"심층분석보고서_{safe_company_name}_{timestamp}.docx"
    file_path = os.path.join(output_path, filename)

    # 문서 생성
    generator.generate(file_path)
    file_size = os.path.getsize(file_path) / 1024

    print(f"      ✓ DOCX 생성 완료\n")

    # 완료
    print("="*60)
    print("✅ 보고서 생성 완료!")
    print("="*60)
    print(f"\n📄 파일 위치: {file_path}")
    print(f"   파일 크기: {file_size:.2f} KB")
    print(f"\n💡 이 보고서는 실제 조사 데이터를 기반으로 작성되었습니다!")
    print(f"   - 기업 최근 동향: ✓")
    print(f"   - 시장 및 경쟁사 분석: ✓")
    print(f"   - 마케팅 전략 조사: ✓\n")

    return {
        'status': 'completed',
        'docx_path': file_path,
        'docx_size': file_size
    }


def print_usage():
    """사용법 출력"""
    print("\n" + "="*60)
    print("📚 사용법")
    print("="*60)
    print("\n1️⃣  조사 준비:")
    print('   python main_research.py "회사명" "URL" --prepare')
    print()
    print("2️⃣  Claude에게 조사 요청:")
    print('   "research_tasks.json 읽고 조사해서')
    print('    research_results.json에 저장해줘"')
    print()
    print("3️⃣  보고서 생성:")
    print('   python main_research.py "회사명" "URL" --generate')
    print()
    print("="*60)
    print("\n예시:")
    print('  python main_research.py "삼성전자" "samsung.com" --prepare')
    print('  (Claude에게 조사 요청)')
    print('  python main_research.py "삼성전자" "samsung.com" --generate')
    print()


def main():
    """메인 함수"""
    # 인자 파싱
    if len(sys.argv) < 4:
        print("\n❌ 오류: 인자가 부족합니다.")
        print_usage()
        return

    company_name = sys.argv[1]
    url = sys.argv[2]
    mode = sys.argv[3]

    # URL 프로토콜 확인
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        if mode == '--prepare':
            # 1단계: 조사 준비
            result = prepare_research(company_name, url)
            return result

        elif mode == '--generate':
            # 3단계: 보고서 생성
            result = generate_report(company_name, url)
            return result

        else:
            print(f"\n❌ 오류: 알 수 없는 모드 '{mode}'")
            print_usage()
            return

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        print(f"자세한 내용:\n")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
