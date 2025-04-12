from utils.io import load_text
import llm_client

def write_chapter_from_answers(subtopic: str, answers: dict, book_context: str, review_points: list) -> str:
    """
    소제목과 질문-응답을 기반으로 하나의 리뷰 챕터(본문)를 생성합니다.
    """
    prompt_template = load_text("prompts/write_chapter.txt")

    formatted_qa = "\n".join([f"질문: {q}\n답변: {a}" for q, a in answers.items()])
    formatted_keywords = "\n".join(f"- {kw}" for kw in review_points)

    prompt = prompt_template.format(
        subtopic=subtopic,
        answers=formatted_qa,
        book_context=book_context,
        review_points=formatted_keywords
    )

    response = llm_client.ask(prompt)
    print(f"✍️ '{subtopic}' 챕터 생성 완료")
    return response.strip()
