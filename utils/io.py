import re

def load_text(file_path: str) -> str:
    """
    주어진 파일의 전체 텍스트를 읽어서 반환합니다.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_text(file_path: str, text: str):
    """
    주어진 텍스트를 파일에 저장합니다.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def parse_list(text: str) -> list:
    """
    문자형 목록을 받아 각 항목을 리스트로 분리합니다 (번호나 불릿 기호 제거).
    """
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # 항목 앞의 불릿 또는 번호 제거
        if line[0] in ['-', '*', '•']:
            item = line[1:].strip()
        else:
            item = re.sub(r'^[\d\.\)\(\s]+', '', line).strip()
        if item:
            items.append(item)
    return items
