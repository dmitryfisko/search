import queue
from collections import Counter
from time import sleep

from site_parser.loader.task import UrlLoaderTask
from site_parser.loader.utils import QueueUrl


class SiteLoader:
    QUEUE_MAX_SIZE = 100
    WORKER_POOL_SIZE = 10

    def __init__(self, coordinator):
        self._coord = coordinator
        self._task_canceled = False

    def cancel_task(self):
        self._task_canceled = True

    def _active_job(self, worker_threads):
        workers_state = [worker.is_active_job() for worker in worker_threads]
        return any(workers_state)

    def start(self, start_url):
        words_counter = Counter()
        que = queue.Queue(maxsize=self.QUEUE_MAX_SIZE)
        worker_threads = self._build_worker_pool(que, words_counter, self.WORKER_POOL_SIZE)

        url = QueueUrl(start_url, 0)
        que.put(url)
        while (que.qsize() or self._active_job(worker_threads)) and not self._task_canceled:
            sleep(0.1)

        for _ in worker_threads:
            que.put('quit')
        for worker in worker_threads:
            worker.join()

    def _build_worker_pool(self, que, words_counter, size):
        workers = []
        for _ in range(size):
            worker = UrlLoaderTask(que, words_counter, self._coord)
            worker.start()
            workers.append(worker)
        return workers
