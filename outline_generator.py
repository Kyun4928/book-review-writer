from utils.io import load_text
import llm_client

def generate_subtopics(user_responses: list, book_context: str, review_points: list, title: str) -> list:
    """
    유저의 감상, 책 정보, 리뷰 키워드를 종합해 GPT에게 리뷰용 소제목 후보를 요청합니다.
    """
    prompt_template = load_text("prompts/subtopics.txt")

    formatted_responses = "\n".join(f"- {resp}" for resp in user_responses)
    formatted_keywords = "\n".join(f"- {rp}" for rp in review_points)

    prompt = prompt_template.format(
        title=title,
        book_context=book_context,
        review_points=formatted_keywords,
        user_responses=formatted_responses
    )

    response = llm_client.ask(prompt)
    subtopics = [line.strip("- ").strip() for line in response.strip().splitlines() if line.strip()]

    print(f"🧩 소제목 후보 {len(subtopics)}개 생성됨.")
    return subtopics