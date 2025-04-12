from utils.io import load_text
import llm_client

def generate_guided_questions(subtopic: str, book_context: str, review_points: list) -> list:
    """
    주어진 소제목에 대해 유저가 글을 전개할 수 있도록 도와주는 질문을 GPT에게 요청합니다.
    """
    prompt_template = load_text("prompts/guided_questions.txt")

    formatted_keywords = "\n".join(f"- {rp}" for rp in review_points)
    prompt = prompt_template.format(
        book_context=book_context,
        review_points=formatted_keywords,
        subtopic=subtopic
    )

    response = llm_client.ask(prompt)
    questions = [line.strip("- ").strip() for line in response.strip().splitlines() if line.strip()]

    print(f"🧭 '{subtopic}' 주제에 대한 질문 {len(questions)}개 생성됨.")
    return questions
