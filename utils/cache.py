import os
import json
import hashlib
import time
from typing import Any, Optional

class Cache:
    """
    캐싱 기능을 제공하는 클래스
    """

    def __init__(self, cache_dir: str = ".cache", expiry_time: int = 86400):
        """
        캐시 초기화

        :param cache_dir: 캐시 파일을 저장할 디렉토리
        :param expiry_time: 캐시 만료 시간 (초 단위, 기본 24시간)
        """
        self.cache_dir = cache_dir
        self.expiry_time = expiry_time

        # 캐시 디렉토리가 없으면 생성
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_key(self, *args, **kwargs) -> str:
        """
        주어진 인자를 기반으로 캐시 키를 생성

        :return: 해시된 캐시 키
        """
        # 인자들을 문자열로 변환
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
        key_str = ":".join(key_parts)

        # SHA-256 해시 사용
        return hashlib.sha256(key_str.encode('utf-8')).hexdigest()

    def _get_cache_path(self, cache_key: str) -> str:
        """
        주어진 캐시 키에 대한 파일 경로 반환

        :param cache_key: 캐시 키
        :return: 캐시 파일 경로
        """
        return os.path.join(self.cache_dir, f"{cache_key}.json")

    def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 값을 가져옴

        :param key: 캐시 키
        :return: 캐시된 값 또는 None (캐시 미스)
        """
        cache_path = self._get_cache_path(key)

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # 만료 시간 확인
            if time.time() - cache_data['timestamp'] > self.expiry_time:
                # 만료된 캐시 삭제
                os.remove(cache_path)
                return None

            return cache_data['value']

        except (json.JSONDecodeError, KeyError):
            # 잘못된 형식의 캐시 파일이면 삭제
            if os.path.exists(cache_path):
                os.remove(cache_path)
            return None

    def set(self, key: str, value: Any) -> None:
        """
        값을 캐시에 저장

        :param key: 캐시 키
        :param value: 저장할 값
        """
        cache_path = self._get_cache_path(key)

        cache_data = {
            'timestamp': time.time(),
            'value': value
        }

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def cached(self, func):
        """
        함수 결과를 캐싱하는 데코레이터

        :param func: 캐싱할 함수
        :return: 캐싱 적용된 함수
        """
        def wrapper(*args, **kwargs):
            # 캐시 비활성화 플래그 확인
            skip_cache = kwargs.pop('skip_cache', False)

            if skip_cache:
                return func(*args, **kwargs)

            # 캐시 키 생성
            cache_key = self._get_cache_key(func.__name__, *args, **kwargs)

            # 캐시에서 값 가져오기
            cached_result = self.get(cache_key)

            if cached_result is not None:
                print(f"[캐시] '{func.__name__}' 함수 결과를 캐시에서 로드했습니다.")
                return cached_result

            # 함수 실행 및 결과 캐싱
            result = func(*args, **kwargs)
            self.set(cache_key, result)

            return result

        return wrapper

    def clear(self, older_than: Optional[int] = None) -> int:
        """
        캐시 파일 정리

        :param older_than: 지정된 시간(초)보다 오래된 캐시만 삭제, None이면 모든 캐시 삭제
        :return: 삭제된 파일 수
        """
        count = 0
        current_time = time.time()

        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue

            file_path = os.path.join(self.cache_dir, filename)

            if older_than is not None:
                # 파일 수정 시간 확인
                file_age = current_time - os.path.getmtime(file_path)
                if file_age <= older_than:
                    continue

            try:
                os.remove(file_path)
                count += 1
            except OSError:
                continue

        return count

# 전역 캐시 인스턴스 생성
cache = Cache()