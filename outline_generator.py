from utils.io import load_text, parse_list
import llm_client

def generate_outline(title: str, book_info_text: str, review_points: list, user_points: list) -> list:
    """
    책 정보, 리뷰 포인트, 독자 관심사를 기반으로 리뷰 아웃라인을 생성합니다.
    """
    # 리뷰 포인트 목록 문자열 생성 (없으면 '없음')
    review_points_str = "없음"
    if review_points:
        review_points_str = "\n".join(f"- {pt}" for pt in review_points)
    # 독자 관심사 목록 문자열 생성 (없으면 '없음')
    user_points_str = "없음"
    if user_points:
        user_points_str = "\n".join(f"- {pt}" for pt in user_points)
    prompt_template = load_text("prompts/subtopics.txt")
    prompt = prompt_template.format(
        title=title,
        book_info=book_info_text.strip(),
        review_points=review_points_str,
        user_points=user_points_str
    )
    result = llm_client.ask(prompt)
    outline_list = parse_list(result)
    return outline_list
