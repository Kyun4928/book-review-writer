from utils.io import load_text
import llm_client
from utils.cache import cache

@cache.cached
def get_book_context(title: str, author: str) -> str:
    """
    책 제목과 저자명을 기반으로 GPT에게 책 정보를 요청해 요약된 맥락을 반환합니다.
    결과는 캐시되어 동일한 요청에 대해 재사용됩니다.
    """
    prompt_template = load_text("prompts/book_info.txt")
    prompt = prompt_template.format(title=title, author=author)
    result = llm_client.ask(prompt)
    return result.strip()