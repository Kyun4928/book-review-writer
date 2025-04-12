import os
import openai
from openai import OpenAI  # 최신 SDK 사용
import time

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OpenAI API key not found. Please set OPENAI_API_KEY.")

client = OpenAI(api_key=openai_api_key)

def ask(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_retries: int = 3) -> str:
    """
    주어진 프롬프트로 OpenAI ChatCompletion API를 호출하고 응답 텍스트를 반환합니다.
    오류 발생 시 재시도합니다.
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except (openai.APIError, openai.APIConnectionError) as e:
            retry_count += 1
            if retry_count == max_retries:
                raise Exception(f"OpenAI API 호출 실패: {e}")
            print(f"API 오류, {retry_count}번째 재시도 중...")
            time.sleep(2)  # 재시도 전 대기
        except Exception as e:
            raise Exception(f"예상치 못한 오류: {e}")