import requests
from bs4 import BeautifulSoup

def get_reviews(title: str) -> list:
    """
    주어진 책 제목을 기반으로 YES24 검색 결과에서 리뷰 텍스트를 크롤링합니다.
    """
    print("📡 YES24에서 리뷰를 수집 중입니다...")

    search_url = f"https://www.yes24.com/Product/Search?domain=BOOK&query={title}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        search_res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(search_res.text, "html.parser")
        first_link = soup.select_one("div.goodsList_info a.gd_name")
        if not first_link:
            print("❌ 책을 찾을 수 없습니다.")
            return []

        book_url = "https://www.yes24.com" + first_link["href"]
        book_res = requests.get(book_url, headers=headers)
        book_soup = BeautifulSoup(book_res.text, "html.parser")

        # 리뷰 영역 찾기
        review_elements = book_soup.select("div.reviewInfoBot.cropContentsReview")
        reviews = [r.get_text(strip=True) for r in review_elements]

        print(f"✅ 리뷰 {len(reviews)}건 수집 완료.")
        return reviews[:10]  # 최대 10개만 반환

    except Exception as e:
        print(f"❌ 리뷰 수집 중 오류 발생: {e}")
        return []