from utils.io import load_text
import llm_client

def write_review(outline: list, questions: list, answers: list) -> str:
    """
    아웃라인, 질문, 답변을 사용하여 최종 책 리뷰 본문을 작성합니다.
    """
    review_sections = []
    prompt_template = load_text("prompts/write_chapter.txt")
    for idx, section in enumerate(outline):
        # 각 섹션에 대응되는 질문과 답변 가져오기 (없을 경우 빈 문자열)
        question = questions[idx] if idx < len(questions) else ""
        answer = answers[idx] if idx < len(answers) else ""
        # 섹션 작성 프롬프트 구성 및 GPT 호출
        prompt = prompt_template.format(section_title=section, question=question, answer=answer)
        section_text = llm_client.ask(prompt)
        review_sections.append(section_text.strip())
    # 모든 섹션 텍스트를 한 개의 문자열로 합치기 (두 줄 띄워 구분)
    final_review = "\n\n".join(review_sections)
    return final_review
