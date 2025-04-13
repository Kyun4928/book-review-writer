import sys
import threading
from book_info import get_book_context
from review_crawler import get_reviews
from review_processor import process_reviews
from outline_generator import generate_subtopics
from utils.io import select_items_from_list, save_review_to_file
from interview import ask_interview_questions, conduct_interview
from question_generator import generate_guided_questions
from review_writer import write_chapter_from_answers
from utils.progress import Progress

def get_valid_input(prompt: str, error_msg: str = "입력이 올바르지 않습니다. 다시 시도해주세요.") -> str:
    """사용자로부터 유효한 입력을 받습니다."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print(error_msg)

def async_task_with_progress(task_func, progress_desc, *args, **kwargs):
    """
    비동기로 작업을 실행하면서 진행 상태를 표시합니다.
    """
    result = [None]
    exception = [None]
    completed = [False]

    def worker():
        try:
            result[0] = task_func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
        finally:
            completed[0] = True

    # 작업 스레드 시작
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

    # 진행 상태 표시
    Progress.indeterminate(desc=progress_desc, callback=lambda: completed[0])

    # 예외 발생 확인
    if exception[0]:
        raise exception[0]

    return result[0]

def main():
    print("📘 책 리뷰 생성기에 오신 걸 환영합니다!")

    # 1. 책 정보 입력
    title = get_valid_input("책 제목을 입력하세요: ", "책 제목은 필수입니다.")
    author = get_valid_input("저자명을 입력하세요: ", "저자명은 필수입니다.")

    # 진행 단계 정의
    steps = [
        "책 정보 수집",
        "리뷰 수집",
        "리뷰 분석",
        "인터뷰 질문 생성",
        "소제목 후보 생성",
        "챕터 작성",
        "최종 리뷰 저장"
    ]

    try:
        # 진행 상태 표시 시작
        Progress.step_progress(steps, 0)

        # 2. 책 정보 요약 (비동기 + 프로그레스 표시)
        book_context = async_task_with_progress(
            get_book_context, 
            f"'{title}' 책 정보 수집 중",
            title, 
            author
        )

        if not book_context:
            raise Exception("책 정보를 가져오는데 실패했습니다.")

        Progress.step_progress(steps, 1)

        # 3. 리뷰 수집 및 키워드 추출 (비동기 + 프로그레스 표시)
        reviews = async_task_with_progress(
            get_reviews,
            f"'{title}' 리뷰 수집 중",
            title,
            author
        )
        if not reviews:
            print("\n⚠️ 리뷰를 수집하지 못했습니다. 리뷰가 없는 책일 수 있습니다.")
            review_points=[]
        else:
            Progress.step_progress(steps, 2)
            # 리뷰 분석
            review_points = async_task_with_progress(
                process_reviews,
                "리뷰 분석 중",
                title,
                reviews
            )

        Progress.step_progress(steps, 3)

        # 5. 인터뷰 질문 생성 (비동기 + 프로그레스 표시)
        questions = async_task_with_progress(
            ask_interview_questions,
            "인터뷰 질문 생성 중",
            book_context,
            review_points,
            title
        )

        # 유저 인터뷰 진행 (동기식 - 사용자 입력 필요)
        user_responses = conduct_interview(book_context, review_points, questions)

        Progress.step_progress(steps, 4)

        # 6. 소제목 후보 생성 (비동기 + 프로그레스 표시)
        subtopic_candidates = async_task_with_progress(
            generate_subtopics,
            "소제목 후보 생성 중",
            user_responses,
            book_context,
            review_points,
            title
        )

        if not subtopic_candidates:
            raise Exception("소제목 생성에 실패했습니다.")

        # 7. 유저가 소제목 선택 (동기식 - 사용자 입력 필요)
        selected_subtopics = select_items_from_list(
            subtopic_candidates,
            "리뷰에 포함할 소제목을 2~5개 선택해주세요:",
            min_select=2,
            max_select=5
        )

        Progress.step_progress(steps, 5)

        # 8. 각 챕터 작성
        chapters = []
        for idx, subtopic in enumerate(selected_subtopics):
            print(f"\n[챕터 {idx+1}/{len(selected_subtopics)}: {subtopic}]")
            print("1. 직접 작성하기")
            print("2. 질문 받고 작성하기 (GPT가 인터뷰 후 챕터 자동 생성)")

            while True:
                mode = input("선택 (1 또는 2): ").strip()
                if mode in ["1", "2"]:
                    break
                print("1 또는 2를 입력해주세요.")

            if mode == "1":
                content = get_valid_input(f"\n'{subtopic}'에 대한 내용을 자유롭게 작성해주세요:\n> ")
                chapters.append({"title": subtopic, "content": content})
            else:
                # GPT가 해당 소제목에 대해 질문 생성 (비동기 + 프로그레스 표시)
                guided_questions = async_task_with_progress(
                    generate_guided_questions,
                    f"'{subtopic}' 주제 질문 생성 중",
                    subtopic,
                    book_context,
                    review_points
                )

                # 사용자 답변 수집 (동기식)
                answers = {}
                print("\n[아래 질문에 답해주세요:]")
                for q_idx, q in enumerate(guided_questions, start=1):
                    print(f"\n[{q_idx}/{len(guided_questions)}] {q}")
                    ans = get_valid_input("> ")
                    answers[q] = ans

                # 챕터 작성 (비동기 + 프로그레스 표시)
                content = async_task_with_progress(
                    write_chapter_from_answers,
                    f"'{subtopic}' 챕터 작성 중",
                    subtopic,
                    answers,
                    book_context,
                    review_points
                )

                chapters.append({"title": subtopic, "content": content})

        Progress.step_progress(steps, 6)

        # 10. 리뷰 조립 및 저장
        final_review = f"# 『{title}』 리뷰\n\n"
        for chapter in chapters:
            final_review += f"## {chapter['title']}\n{chapter['content']}\n\n"

        filename = f"{title}_review.txt"
        save_review_to_file(final_review, filename=filename)

        Progress.step_progress(steps, 7)  # 완료

        print("\n✅ 리뷰가 성공적으로 생성되어 저장되었습니다!")
        print(f"📄 파일명: {filename}")

    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()