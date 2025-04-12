from utils.io import load_text, parse_list
import llm_client

def get_user_keywords(book_info_text: str, title: str) -> list:
    """
    책 정보로부터 독자가 궁금해할 만한 포인트를 LLM으로 추론하여 반환합니다.
    """
    prompt_template = load_text("prompts/user_keywords.txt")
    prompt = prompt_template.format(title=title, summary=book_info_text)
    result = llm_client.ask(prompt)
    user_points = parse_list(result)
    return user_points

def filter_points(review_points: list, user_points: list) -> list:
    """
    리뷰 기반 포인트와 독자 관심사를 합쳐 하나의 핵심 포인트 리스트로 만듭니다.
    (중복 제거)
    """
    combined = []
    for p in review_points:
        if p not in combined:
            combined.append(p)
    for p in user_points:
        if p not in combined:
            combined.append(p)
    return combined
