from concurrent.futures.thread import ThreadPoolExecutor
from core.fast_extractor import UltraFastExtractor

def extract_resumes_parallel(texts, max_workers = 4):
    extractor = UltraFastExtractor()

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        results = list(ex.map(extractor.extract, texts))

    return results