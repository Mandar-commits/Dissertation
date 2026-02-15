import time
from dataclasses import dataclass

@dataclass()
class ExtractionMetrics:
    total_time: float = 0
    fast_path_time: float = 0
    llm_time: float = 0
    embedding_time: float = 0
    text_length: int = 0
    llm_called: bool = False

class PerformanceTracker:
    def __init__(self):
        self.metrics = ExtractionMetrics()
        self._start = time.time()

    def mark_fast_path(self):
        self.metrics.fast_path_time = time.time() - self._start

    def mark_llm(self, start_time):
        self.metrics.llm_time = time.time() - start_time
        self.metrics.llm_called = True

    def finalize(self):
        self.metrics.total_time = time.time() - self._start
        return self.metrics