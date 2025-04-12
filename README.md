# 책 리뷰 생성기 (Book Review Generator)

## 소개
이 프로젝트는 사용자가 책 제목을 입력하면, 해당 책에 대한 정보를 수집하고 독자들의 리뷰를 분석하여, 인공지능을 통해 종합적인 책 리뷰를 자동으로 생성해주는 프로그램입니다. OpenAI의 GPT 언어 모델을 활용하여 책의 기본 정보 수집부터 리뷰 요약, 인터뷰 형식의 내용 생성, 최종 리뷰 작성까지 여러 단계를 거쳐 결과물을 만들어냅니다.

## 구성 파일
- **main.py**: 프로그램의 진입점으로, 각 단계별 함수를 호출하여 전체 흐름을 제어합니다.
- **book_info.py**: 책의 제목을 바탕으로 책의 저자, 장르, 줄거리 요약 등의 정보를 얻습니다.
- **review_crawler.py**: 웹에서 해당 책에 대한 독자 리뷰를 수집합니다 (Goodreads 사용).
- **review_processor.py**: 수집된 리뷰를 요약하고 공통 핵심 의견을 추출합니다.
- **semantic_filter.py**: 리뷰에서 추출된 포인트와 독자 관심사를 종합하여 중요한 주제 리스트를 만듭니다.
- **outline_generator.py**: 책 리뷰의 아웃라인(구성)을 생성합니다.
- **question_generator.py**: 각 아웃라인 섹션에 대한 핵심 질문을 생성합니다.
- **interview.py**: 생성된 질문들을 바탕으로 인공지능과 질의응답을 수행하여 세부 정보를 얻습니다.
- **review_writer.py**: 아웃라인과 Q&A로부터 최종 리뷰 텍스트를 작성합니다.
- **llm_client.py**: OpenAI API를 호출하는 클라이언트로, GPT 모델에게 프롬프트를 보내고 응답을 받는 기능을 제공합니다.
- **utils/io.py**: 파일 입출력 및 텍스트 파싱 관련 유틸 함수들을 제공합니다 (프롬프트 불러오기, 리스트 파싱 등).

또한 `prompts/` 디렉터리에 각 단계별로 OpenAI에 보낼 프롬프트 템플릿이 저장되어 있습니다:
- prompts/book_info.txt
- prompts/review_keywords.txt
- prompts/user_keywords.txt
- prompts/subtopics.txt
- prompts/guided_questions.txt
- prompts/write_chapter.txt

그리고 Replit 환경설정을 위한 파일들:
- **.gitignore**: Git에 포함하지 않을 파일 목록.
- **.replit**: Replit에서 실행 환경을 정의하는 설정.
- **replit.nix**: Replit에서 nix 환경으로 필요한 패키지(Python 등)를 명시.
- **requirements.txt**: 필요한 파이썬 패키지 목록(OpenAI API, requests, BeautifulSoup 등).
- **README.md**: 프로젝트 설명서 (바로 이 문서).

## 사용 방법
1. OpenAI API 키를 준비합니다. Replit에서 해당 Repl을 포크하거나 업로드한 후, **Secrets** 설정에서 `OPENAI_API_KEY` 환경변수에 본인의 OpenAI API 키를 추가하세요.
2. Replit에서 Run 버튼을 눌러 프로그램을 실행합니다 (또는 터미널에서 `python main.py`).
3. 실행 후 터미널에 표시되는 안내에 따라 리뷰를 생성할 책의 제목을 입력합니다.
4. 프로그램이 여러 단계를 거쳐 책 리뷰를 생성하며, 완료되면 콘솔에 최종 리뷰가 출력됩니다. 또한 생성된 리뷰는 `review_output.txt` 파일로 저장되어 나중에 열람할 수도 있습니다.

## 참고 사항
- 이 프로그램은 인터넷에서 Goodreads 리뷰를 스크래핑하여 데이터를 수집하므로, Replit에서 인터넷 접근이 가능해야 합니다. (일부 환경에서는 외부 웹 요청이 제한될 수 있습니다.)
- OpenAI API를 호출하여 결과를 생성하므로, API 사용량과 비용에 유의하세요.
- 생성된 책 리뷰 내용은 인공지능 모델의 응답을 기반으로 하므로 실제 책의 내용과 완전히 일치하지 않을 수 있습니다. 중요한 사실 정보는 별도로 확인하는 것이 좋습니다.
- 리뷰 생성 과정에서 다단계의 프롬프트를 사용하기 때문에 시간이 다소 소요될 수 있습니다 (수십 초 정도). 실행 중 단계별로 상태 메시지를 출력하니 참고하시기 바랍니다.
