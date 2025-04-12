from book_info import get_book_context
from review_crawler import get_reviews
from review_processor import process_reviews
from outline_generator import generate_subtopics
from utils.io import select_items_from_list, save_review_to_file
from interview import ask_interview_questions, conduct_interview
from question_generator import generate_guided_questions
from review_writer import write_chapter_from_answers

print("📘 책 리뷰 생성기에 오신 걸 환영합니다!")

# 1. 책 정보 입력
title = input("책 제목을 입력하세요: ").strip()
author = input("저자명을 입력하세요: ").strip()
print("\n[책 정보 수집 중...]\n")

# 2. 책 정보 요약
book_context = get_book_context(title, author)

# 3. 리뷰 수집 및 키워드 추출
reviews = get_reviews(title)
review_points = process_reviews(title, reviews)

# 5. 유저가 인터뷰 응답
questions = ask_interview_questions(book_context, review_points, title)
user_responses = conduct_interview(book_context, review_points, questions)

# 6. 유저 응답 + 책 정보 + 리뷰 키워드 기반으로 소제목 후보 생성
subtopic_candidates = generate_subtopics(user_responses, book_context, review_points, title)

# 7. 유저가 소제목 선택
selected_subtopics = select_items_from_list(
    subtopic_candidates,
    "리뷰에 포함할 소제목을 2~5개 선택해주세요:",
    min_select=2,
    max_select=5
)

# 8. 각 챕터 작성
chapters = []
for subtopic in selected_subtopics:
    print(f"\n[챕터: {subtopic}]")
    print("1. 직접 작성하기")
    print("2. 질문 받고 작성하기 (GPT가 인터뷰 후 챕터 자동 생성)")
    mode = input("선택 (1 또는 2): ").strip()

    if mode == "1":
        content = input(f"\n'{subtopic}'에 대한 내용을 자유롭게 작성해주세요:\n> ")
    else:
        # GPT가 해당 소제목에 대해 질문 생성
        guided_questions = generate_guided_questions(subtopic, book_context, review_points)
        answers = {}
        print("\n[아래 질문에 답해주세요:]")
        for idx, q in enumerate(guided_questions, start=1):
            print(f"\n[{idx}/{len(guided_questions)}] {q}")
            ans = input("> ")
            answers[q] = ans.strip()
        content = write_chapter_from_answers(subtopic, answers, book_context, review_points)

    chapters.append({"title": subtopic, "content": content})

# 10. 리뷰 조립 및 저장
final_review = f"# 『{title}』 리뷰\n\n"
for chapter in chapters:
    final_review += f"## {chapter['title']}\n{chapter['content']}\n\n"

save_review_to_file(final_review, filename=f"{title}_review.txt")
print("\n✅ 리뷰가 성공적으로 생성되어 저장되었습니다!")
print(f"📄 파일명: {title}_review.txt")