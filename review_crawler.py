import requests
from bs4 import BeautifulSoup
import re
from utils.cache import cache

@cache.cached
def get_reviews(title: str, author: str, max_reviews: int = 10, timeout: int = 10) -> list:
    """
    주어진 책 제목을 기반으로 YES24 검색 결과에서 리뷰 텍스트를 크롤링합니다.
    책 ID를 추출하여 리뷰 페이지에 직접 접근하는 방식으로 개선되었습니다.
    결과는 캐시되어 동일한 요청에 대해 재사용됩니다.
    """
    if not title:
        print("❌ 책 제목이 입력되지 않았습니다.")
        return []

    print("📡 YES24에서 리뷰를 수집 중입니다...")

    try:
        # 1. 검색 페이지 접근
        search_url = f"https://www.yes24.com/Product/Search?domain=BOOK&query={author}%20{title}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        search_res = requests.get(search_url, headers=headers, timeout=timeout)
        search_res.raise_for_status()  # HTTP 오류 확인

        # 2. 검색 결과 파싱하여 첫 번째 책의 data-goods-no 속성 찾기
        soup = BeautifulSoup(search_res.text, "html.parser")
        first_item = soup.select_one("li[data-goods-no]")

        if not first_item:
            print("❌ 책을 찾을 수 없습니다. 검색 결과가 없거나 웹사이트 구조가 변경되었습니다.")
            return []

        # 3. data-goods-no 속성에서 상품 ID 추출
        goods_id = first_item.get("data-goods-no")
        if not goods_id:
            print("❌ 상품 ID를 추출할 수 없습니다.")
            return []

        print(f"✓ 상품 ID: {goods_id}")

        # 4. 책 상세 URL 생성
        book_url = f"https://www.yes24.com/Product/Goods/{goods_id}"
        print(f"✓ 책 URL: {book_url}")

        # 5. 리뷰 페이지 직접 접근
        review_url = f"https://www.yes24.com/Product/communityModules/GoodsReviewList/{goods_id}"
        print(f"✓ 리뷰 URL: {review_url}")

        review_res = requests.get(review_url, headers=headers, timeout=timeout)
        if review_res.status_code != 200:
            # 첫 번째 시도가 실패하면 대체 URL 형식 시도
            review_url = f"https://www.yes24.com/Product/communityModules/GoodsReviewList?GoodsNumber={goods_id}"
            print(f"✓ 대체 리뷰 URL 시도: {review_url}")
            review_res = requests.get(review_url, headers=headers, timeout=timeout)
            review_res.raise_for_status()

        # 5. 리뷰 페이지 파싱
        review_soup = BeautifulSoup(review_res.text, "html.parser")

        # 6. 다양한 가능한 선택자로 리뷰 찾기
        possible_selectors = [
            "div.reviewInfoBot.cropContentsReview",  # 원래 선택자
            "div.review_cont",                       # 내용 컨테이너
            "ul.reviewList li p.review_cont",        # 리스트 형태 선택자
            "div.reviewInfoBot p",                   # 정보 블록 내 단락
            "div.reviewInfoWrap div.reviewInfoBot",  # 래퍼 내부 선택자
            "p.reviewContent"                        # 내용 단락
        ]

        reviews = []
        for selector in possible_selectors:
            review_elements = review_soup.select(selector)
            if review_elements:
                print(f"✓ 선택자 '{selector}'로 리뷰 요소 {len(review_elements)}개를 찾았습니다.")
                temp_reviews = [r.get_text(strip=True) for r in review_elements if r.get_text(strip=True)]
                if temp_reviews:
                    reviews = temp_reviews
                    break

        # 7. 여전히 리뷰를 찾지 못한 경우, 상세 페이지 접근하여 시도
        if not reviews:
            print("ℹ️ 리뷰 페이지에서 리뷰를 찾지 못했습니다. 상세 페이지에서 시도합니다.")
            book_res = requests.get(book_url, headers=headers, timeout=timeout)
            book_soup = BeautifulSoup(book_res.text, "html.parser")

            # 상세 페이지에서 리뷰 섹션 찾기
            for selector in possible_selectors:
                review_elements = book_soup.select(selector)
                if review_elements:
                    print(f"✓ 상세 페이지에서 선택자 '{selector}'로 리뷰 찾음")
                    temp_reviews = [r.get_text(strip=True) for r in review_elements if r.get_text(strip=True)]
                    if temp_reviews:
                        reviews = temp_reviews
                        break

        # 8. 결과 반환
        if reviews:
            print(f"✅ 리뷰 {len(reviews)}건 수집 완료.")
            return reviews[:max_reviews]  # 최대 max_reviews개만 반환
        else:
            print("❌ 웹페이지에서 리뷰를 찾을 수 없습니다.")
            # 디버깅 파일 저장
            with open("review_page_debug.html", "w", encoding="utf-8") as f:
                f.write(review_soup.prettify())
            print("ℹ️ 디버깅을 위해 review_page_debug.html 파일에 페이지를 저장했습니다.")
            return []

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
        # 오류의 세부 정보 출력
        import traceback
        print(traceback.format_exc())
        return []