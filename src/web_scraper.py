"""
웹 스크래핑 모듈
기업 웹사이트에서 정보를 수집합니다.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, List


class WebScraper:
    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_website(self) -> Dict[str, any]:
        """
        웹사이트를 스크래핑하여 기업 정보를 수집합니다.
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # 메타 정보 추출
            meta_description = self._get_meta_description(soup)
            meta_keywords = self._get_meta_keywords(soup)

            # 페이지 제목
            title = soup.title.string if soup.title else "제목 없음"

            # 본문 텍스트 추출
            text_content = self._extract_text_content(soup)

            # 주요 헤딩 추출
            headings = self._extract_headings(soup)

            # 링크 분석
            internal_links = self._analyze_links(soup)

            return {
                'url': self.url,
                'domain': self.domain,
                'title': title,
                'meta_description': meta_description,
                'meta_keywords': meta_keywords,
                'text_content': text_content,
                'headings': headings,
                'internal_links': internal_links,
                'status': 'success'
            }

        except requests.exceptions.RequestException as e:
            return {
                'url': self.url,
                'status': 'error',
                'error_message': str(e)
            }

    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """메타 설명 추출"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        return meta_desc.get('content', '') if meta_desc else ''

    def _get_meta_keywords(self, soup: BeautifulSoup) -> str:
        """메타 키워드 추출"""
        meta_kw = soup.find('meta', attrs={'name': 'keywords'})
        return meta_kw.get('content', '') if meta_kw else ''

    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """본문 텍스트 추출 (스크립트, 스타일 제외)"""
        # 스크립트와 스타일 제거
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()

        # 텍스트 추출
        text = soup.get_text(separator=' ', strip=True)
        # 공백 정리
        text = ' '.join(text.split())
        # 처음 3000자만 반환
        return text[:3000]

    def _extract_headings(self, soup: BeautifulSoup) -> List[str]:
        """주요 헤딩(h1, h2, h3) 추출"""
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text and len(text) > 0:
                    headings.append(f"{tag.upper()}: {text}")
        return headings[:10]  # 상위 10개만

    def _analyze_links(self, soup: BeautifulSoup) -> List[str]:
        """내부 링크 분석"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(self.url, href)

            # 같은 도메인의 링크만 수집
            if urlparse(full_url).netloc == self.domain:
                link_text = link.get_text(strip=True)
                if link_text:
                    links.append(f"{link_text} ({full_url})")

        return links[:15]  # 상위 15개만
