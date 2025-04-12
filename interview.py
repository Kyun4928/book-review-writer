from utils.io import load_text
import llm_client

def ask_interview_questions(book_context: str, review_points: list, title: str) -> list:
    """
    유저가 감상을 정리할 수 있도록 돕는 인터뷰 질문을 GPT가 생성합니다.
    """
    prompt_template = load_text("prompts/interview_questions.txt")
    formatted_keywords = "\n".join(f"- {kw}" for kw in review_points)

    prompt = prompt_template.format(
        title=title,
        book_context=book_context,
        review_points=formatted_keywords
    )

    response = llm_client.ask(prompt)
    questions = [line.strip("- ").strip() for line in response.strip().splitlines() if line.strip()]

    print(f"💬 인터뷰 질문 {len(questions)}개 생성됨.")
    return questions

def conduct_interview(book_info_text: str, key_points: list, questions: list) -> list:
    """
    GPT가 생성한 질문을 유저에게 보여주고,
    유저가 직접 답변을 입력하게 한다.
    그 답변을 리스트로 저장하여 이후 리뷰 작성에 활용한다.
    """
    print("\n🗣️ [인터뷰 시작] 아래 질문에 자유롭게 답변해주세요.\n")

    # 참고 정보(책 요약, 키워드)는 내부적으로만 사용
    context = f"책 정보:\n{book_info_text.strip()}\n"
    if key_points:
        context += "\n관련 키워드:\n" + "\n".join(f"- {k}" for k in key_points)

    answers = []
    for idx, question in enumerate(questions, start=1):
        print(f"{idx}. {question}")
        user_answer = input("> ")
        answers.append(user_answer.strip())

    return answers