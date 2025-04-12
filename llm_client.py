import os
import openai

# OpenAI API 키 설정 (환경변수에서 불러오기)
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise EnvironmentError("OpenAI API key not found. Please set OPENAI_API_KEY.")

def ask(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """
    주어진 프롬프트로 OpenAI ChatCompletion API를 호출하고 응답 텍스트를 반환합니다.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=1000
    )
    answer = response["choices"][0]["message"]["content"].strip()
    return answer
