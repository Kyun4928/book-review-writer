import time
import sys
from tqdm import tqdm

class Progress:
    """
    프로그레스 표시를 위한 클래스
    일반 진행률 표시, 스피너, 타이머 등 다양한 형태의 진행 상태를 표시
    """

    @staticmethod
    def spinner(desc="처리 중", total_time=None):
        """스피너 형태의 진행 상태를 표시합니다."""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        i = 0

        try:
            while total_time is None or time.time() - start_time < total_time:
                sys.stdout.write(f"\r{spinner_chars[i % len(spinner_chars)]} {desc}... ")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1

            # 종료 시 줄바꿈
            if total_time is not None:
                sys.stdout.write("\r✓ 완료!      \n")
                sys.stdout.flush()

        except KeyboardInterrupt:
            sys.stdout.write("\r  중단됨        \n")
            sys.stdout.flush()
            raise

    @staticmethod
    def progress_bar(iterable=None, desc="진행 중", total=None):
        """tqdm을 사용한 프로그레스 바를 반환합니다."""
        return tqdm(
            iterable=iterable, 
            desc=desc, 
            total=total, 
            ncols=80, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        )

    @staticmethod
    def indeterminate(desc="작업 중", max_time=None, callback=None):
        """
        시간이 정해지지 않은 작업의 진행 상태를 표시합니다.
        callback 함수가 True를 반환하면 진행을 멈춥니다.
        """
        start_time = time.time()
        stages = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        i = 0

        try:
            while True:
                elapsed = time.time() - start_time

                # 최대 시간 체크
                if max_time and elapsed > max_time:
                    break

                # 콜백 체크
                if callback and callback():
                    break

                # 진행 상태 출력
                minutes, seconds = divmod(int(elapsed), 60)
                time_str = f"{minutes:02d}:{seconds:02d}"
                sys.stdout.write(f"\r{stages[i % len(stages)]} {desc} ({time_str}) ")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1

            # 종료 메시지
            sys.stdout.write("\r✓ 완료!                      \n")
            sys.stdout.flush()

        except KeyboardInterrupt:
            sys.stdout.write("\r  중단됨                     \n")
            sys.stdout.flush()
            raise

    @staticmethod
    def step_progress(steps, current_step=0):
        """단계별 진행 상태를 표시합니다."""
        total_steps = len(steps)
        progress = current_step / total_steps * 100 if total_steps > 0 else 0

        sys.stdout.write(f"\r[{progress:3.0f}%] 단계 {current_step}/{total_steps}: {steps[current_step] if current_step < total_steps else '완료'}")
        sys.stdout.flush()

        if current_step >= total_steps:
            sys.stdout.write("\n")
            sys.stdout.flush()