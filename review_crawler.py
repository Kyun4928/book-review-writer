import requests
from bs4 import BeautifulSoup
from utils.cache import cache

@cache.cached
def get_reviews(title: str, max_reviews: int = 10, timeout: int = 10) -> list:
    """
    주어진 책 제목을 기반으로 YES24 검색 결과에서 리뷰 텍스트를 크롤링합니다.
    결과는 캐시되어 동일한 요청에 대해 재사용됩니다.
    """
    if not title:
        print("❌ 책 제목이 입력되지 않았습니다.")
        return []

    print("📡 YES24에서 리뷰를 수집 중입니다...")

    search_url = f"https://www.yes24.com/Product/Search?domain=BOOK&query={title}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        search_res = requests.get(search_url, headers=headers, timeout=timeout)
        search_res.raise_for_status()  # HTTP 오류 확인

        soup = BeautifulSoup(search_res.text, "html.parser")
        first_link = soup.select_one("div.goodsList_info a.gd_name")
        if not first_link:
            print("❌ 책을 찾을 수 없습니다.")
            return []

        book_url = "https://www.yes24.com" + first_link["href"]
        book_res = requests.get(book_url, headers=headers, timeout=timeout)
        book_res.raise_for_status()

        book_soup = BeautifulSoup(book_res.text, "html.parser")

        # 리뷰 영역 찾기
        review_elements = book_soup.select("div.reviewInfoBot.cropContentsReview")
        reviews = [r.get_text(strip=True) for r in review_elements if r.get_text(strip=True)]

        print(f"✅ 리뷰 {len(reviews)}건 수집 완료.")
        return reviews[:max_reviews]  # 최대 max_reviews개만 반환

    except requests.exceptions.Timeout:
        print("❌ 리뷰 수집 시간이 초과되었습니다.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 오류: {e}")
        return []
    except requests.exceptions.ConnectionError:
        print("❌ 서버 연결에 실패했습니다.")
        return []
    except Exception as e:
        print(f"❌ 리뷰 수집 중 오류 발생: {e}")
        return []