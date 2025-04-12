import llm_client

def conduct_interview(book_info_text: str, key_points: list, questions: list) -> list:
    """
    책 정보와 핵심 포인트를 배경 지식으로 하여, 각 질문에 대한 답변을 생성합니다.
    """
    answers = []
    # 맥락(Context) 설정: 책 정보 + 핵심 포인트 목록
    context = f"책 정보:\n{book_info_text.strip()}\n\n"
    if key_points:
        context += "관련 핵심 포인트:\n"
        for p in key_points:
            context += f"- {p}\n"
        context += "\n"
    # 각 질문에 대해 GPT에게 답변 요청
    for question in questions:
        prompt = context + f"질문: {question}\n답변:"
        answer = llm_client.ask(prompt)
        answers.append(answer.strip())
    return answers
