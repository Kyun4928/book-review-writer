from utils.io import load_text, parse_list
import llm_client

def generate_questions(outline: list, review_points: list, user_points: list) -> list:
    """
    아웃라인과 포인트들을 참고하여 각 섹션에 대한 가이드 질문 리스트를 생성합니다.
    """
    # 아웃라인 목록을 번호 붙은 문자열로 변환
    outline_str = "\n".join(f"{idx+1}. {sec}" for idx, sec in enumerate(outline))
    # 리뷰 포인트 문자열
    review_points_str = "없음"
    if review_points:
        review_points_str = "\n".join(f"- {pt}" for pt in review_points)
    # 독자 관심사 문자열
    user_points_str = "없음"
    if user_points:
        user_points_str = "\n".join(f"- {pt}" for pt in user_points)
    prompt_template = load_text("prompts/guided_questions.txt")
    prompt = prompt_template.format(
        outline=outline_str,
        review_points=review_points_str,
        user_points=user_points_str
    )
    result = llm_client.ask(prompt)
    questions = parse_list(result)
    return questions
