import sys
import time


class ProgressBar:
    def __init__(self, total=100, prefix='', suffix='', length=50, fill='█'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.current = 0

    def update(self, progress=None):
        """Обновить прогресс-бар"""
        if progress is not None:
            self.current = progress

        percent = ("{0:.1f}").format(100 * (self.current / float(self.total)))
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)

        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}')
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def increment(self, step=1):
        """Увеличить прогресс на шаг"""
        self.current += step
        if self.current > self.total:
            self.current = self.total
        self.update()

    def finish(self):
        """Завершить прогресс-бар"""
        self.current = self.total
        self.update()


def simulate_progress(prefix='Progress', total=100, delay=0.1):
    """Имитация прогресса для тестирования"""
    bar = ProgressBar(total=total, prefix=prefix, suffix='Complete', length=50)
    for i in range(total + 1):
        time.sleep(delay)
        bar.update(i)