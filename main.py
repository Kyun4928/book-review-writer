import book_info
import review_crawler
import review_processor
import semantic_filter
import outline_generator
import question_generator
import interview
import review_writer
from utils.io import save_text

if __name__ == "__main__":
    # 1. 사용자로부터 책 제목 입력 받기
    title = input("책 제목을 입력하세요: ").strip()
    if not title:
        print("책 제목을 입력하지 않아 프로그램을 종료합니다.")
        exit(0)
    print("책 정보 수집 중...")

    # 2. 책 기본 정보 가져오기 (저자, 장르, 줄거리 등)
    book_info_text = book_info.get_book_info(title)

    # 3. 책 정보를 바탕으로 독자 관심사 키워드 생성
    print("독자 관심사 분석 중...")
    user_points = semantic_filter.get_user_keywords(book_info_text, title)

    # 4. 해당 책의 독자 리뷰 크롤링
    print("독자 리뷰 수집 중...")
    reviews = review_crawler.get_reviews(title)

    # 5. 리뷰 내용 요약 및 핵심 포인트 추출
    print("리뷰 분석 중...")
    review_points = review_processor.process_reviews(title, reviews)

    # 6. 리뷰 포인트와 독자 관심사를 통합 (semantic filter)
    combined_points = semantic_filter.filter_points(review_points, user_points)

    # 7. 책 리뷰 아웃라인 생성
    print("아웃라인 생성 중...")
    outline = outline_generator.generate_outline(title, book_info_text, review_points, user_points)

    # 8. 각 아웃라인 섹션에 대한 가이드 질문 생성
    print("가이드 질문 생성 중...")
    questions = question_generator.generate_questions(outline, review_points, user_points)

    # 9. 생성된 질문으로 인터뷰(질의응답) 수행하여 답변 얻기
    print("인터뷰 진행 중...")
    answers = interview.conduct_interview(book_info_text, combined_points, questions)

    # 10. 아웃라인과 Q&A를 바탕으로 최종 리뷰 작성
    print("리뷰 작성 중...")
    final_review = review_writer.write_review(outline, questions, answers)

    # 11. 최종 생성된 리뷰 출력
    print("\n생성된 책 리뷰:\n")
    print(final_review)

    # 12. 리뷰를 파일로 저장
    save_text("review_output.txt", final_review)
    print("\n(리뷰가 review_output.txt 파일에도 저장되었습니다.)")
