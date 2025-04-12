import requests
from bs4 import BeautifulSoup

def get_reviews(title: str) -> list:
    """
    책 제목으로 인터넷에서 독자 리뷰들을 가져옵니다 (예: Goodreads 검색).
    """
    reviews = []
    try:
        # Goodreads에서 책 검색
        search_url = f"https://www.goodreads.com/search?q={requests.utils.requote_uri(title)}"
        resp = requests.get(search_url, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # 첫번째 검색 결과의 책 페이지로 이동
            first_result = soup.find("a", class_="bookTitle")
            if first_result and 'href' in first_result.attrs:
                book_page_url = "https://www.goodreads.com" + first_result['href']
                page = requests.get(book_page_url, timeout=10)
                if page.status_code == 200:
                    soup_book = BeautifulSoup(page.text, "html.parser")
                    # 리뷰 텍스트 부분 추출 (상위 5개 리뷰만)
                    review_elems = soup_book.find_all("div", {"class": "reviewText"})
                    if not review_elems:
                        review_elems = soup_book.find_all("div", {"class": "reviewText stacked"})
                    for elem in review_elems[:5]:
                        text = elem.get_text(separator=" ", strip=True)
                        if text:
                            reviews.append(text)
    except Exception as e:
        print(f"(리뷰 수집 중 오류: {e})")
    # 리뷰를 찾지 못한 경우 reviews 리스트는 빈 상태로 반환됩니다.
    return reviews
