from utils.io import load_text, parse_list
import llm_client

def process_reviews(title: str, reviews: list) -> list:
    """
    수집된 리뷰 텍스트를 요약하고, 자주 언급되는 핵심 의견을 추출합니다.
    """
    if not reviews:
        # 리뷰가 없는 경우 빈 리스트 반환
        return []
    # 리뷰들을 하나의 문자열로 정리 (번호 포함)
    reviews_text = ""
    for idx, rev in enumerate(reviews, start=1):
        reviews_text += f"리뷰 {idx}: {rev}\n"
    prompt_template = load_text("prompts/review_keywords.txt")
    prompt = prompt_template.format(title=title, reviews=reviews_text.strip())
    result = llm_client.ask(prompt)
    points = parse_list(result)
    return points
