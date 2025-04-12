from utils.io import load_text
import llm_client

def get_book_info(title: str) -> str:
    """
    주어진 책 제목에 대한 기본 정보를 LLM을 통해 받아옵니다.
    """
    prompt_template = load_text("prompts/book_info.txt")
    prompt = prompt_template.format(title=title)
    result = llm_client.ask(prompt)
    return result.strip()
