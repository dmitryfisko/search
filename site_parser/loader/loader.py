import queue
from collections import Counter
from time import sleep

from site_parser.loader.task import UrlLoaderTask
from site_parser.loader.utils import QueueUrl, extract_domain, get_or_create_site_model, UNLIMITED_DEPTH


class SiteLoader:
    QUEUE_MAX_SIZE = 100
    WORKER_POOL_SIZE = 10

    def __init__(self, coordinator):
        self._coord = coordinator
        self._task_canceled = False

    def cancel_task(self):
        self._task_canceled = True

    @staticmethod
    def _active_job(worker_threads):
        workers_state = [worker.is_active_job() for worker in worker_threads]
        return any(workers_state)

    def _add_to_site_words_frequency(self, site, words_counter):
        if self._coord.max_depth < UNLIMITED_DEPTH:
            return

        site.clear_dict()
        site.set_words_frequency(words_counter)

    def start(self, start_url):
        self._coord.domain = extract_domain(start_url)
        site = get_or_create_site_model(self._coord.domain)
        site.parse_iteration += 1
        self._coord.parse_iteration = site.parse_iteration

        words_counter = Counter()
        que = queue.Queue(maxsize=self.QUEUE_MAX_SIZE)
        worker_threads = self._build_worker_pool(que, words_counter, site, self.WORKER_POOL_SIZE)

        url = QueueUrl(start_url, 0)
        que.put(url)
        while (que.qsize() or self._active_job(worker_threads)) and not self._task_canceled:
            sleep(0.1)

        for _ in worker_threads:
            que.put('quit')
        for worker in worker_threads:
            worker.join()

        self._add_to_site_words_frequency(site, words_counter)
        site.save()

    def _build_worker_pool(self, que, words_counter, site, pool_size):
        workers = []
        for _ in range(pool_size):
            worker = UrlLoaderTask(que, words_counter, site, self._coord)
            worker.start()
            workers.append(worker)
        return workers
