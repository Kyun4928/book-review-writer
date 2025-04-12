import re

def load_text(filepath: str) -> str:
    """텍스트 파일을 읽어 문자열로 반환합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filepath}")
    except Exception as e:
        raise Exception(f"파일 로드 중 오류 발생: {e}")

def parse_list(text: str) -> list:
    """
    정규 표현식을 사용하여 문자열에서 번호 매긴 항목이나 불릿 포인트를 리스트로 파싱합니다.
    """
    if not text:
        return []

    # 숫자 + 점(.) + 공백으로 시작하거나, 불릿(-,*,•) + 공백으로 시작하는 라인 찾기
    pattern = r'(?:^|\n)(?:\d+\.\s+|\-\s+|\*\s+|•\s+)(.*?)(?=\n|$)'
    matches = re.findall(pattern, text)

    if matches:
        return [match.strip() for match in matches]
    else:
        # 패턴 매칭 실패 시 줄바꿈으로 분리된 비어있지 않은 라인을 반환
        return [line.strip() for line in text.strip().split('\n') if line.strip()]

def select_items_from_list(items: list, prompt_text: str, min_select: int = 1, max_select: int = None) -> list:
    """
    사용자에게 리스트에서 항목을 선택하게 하고 선택된 항목들을 반환합니다.
    """
    if not items:
        print("선택할 항목이 없습니다.")
        return []

    if max_select is None:
        max_select = len(items)

    max_select = min(max_select, len(items))

    print(f"\n{prompt_text}")
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item}")

    while True:
        try:
            selection = input(f"선택할 번호를 쉼표로 구분하여 입력하세요 ({min_select}~{max_select}개): ")
            # 정규 표현식으로 숫자만 추출
            indices = [int(idx) - 1 for idx in re.findall(r'\d+', selection)]

            # 인덱스 유효성 검사
            if any(idx < 0 or idx >= len(items) for idx in indices):
                print("잘못된 번호가 포함되어 있습니다.")
                continue

            # 중복 제거
            selected = [items[idx] for idx in sorted(set(indices))]

            # 선택 개수 검사
            if len(selected) < min_select or len(selected) > max_select:
                print(f"{min_select}~{max_select}개 사이로 선택해주세요.")
                continue

            return selected

        except ValueError:
            print("숫자와 쉼표만 입력해주세요.")
        except Exception as e:
            print(f"오류 발생: {e}")

def save_review_to_file(review_text: str, filename: str = "review_output.txt") -> bool:
    """
    생성된 리뷰를 텍스트 파일로 저장합니다.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(review_text)
        return True
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")
        return False