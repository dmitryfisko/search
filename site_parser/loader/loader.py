import queue
from collections import Counter
from time import sleep

from site_parser.loader.task import UrlLoaderTask
from site_parser.loader.utils import QueueItem, Utils, UNLIMITED_DEPTH, UrlManager


class SiteLoader:
    # QUEUE_MAX_SIZE = 100
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
        if self._coord.depth_limit < UNLIMITED_DEPTH:
            return

        site.clear_dict()
        site.set_words_frequency(words_counter)

    @staticmethod
    def _add_first_queue_item(url, que, url_manager):
        queue_item = QueueItem(url, 0)
        url_manager.add(url)
        que.put(queue_item)

    def start(self, start_url):
        domain = Utils.extract_domain(start_url)
        site = Utils.get_or_create_site_model(domain)

        que = queue.Queue()
        url_manager = UrlManager()
        worker_threads = self._build_worker_pool(que, url_manager, site)

        self._add_first_queue_item(start_url, que, url_manager)
        while (que.qsize() or self._active_job(worker_threads)) and not self._task_canceled:
            sleep(0.1)

        for _ in worker_threads:
            que.put('quit')
        for worker in worker_threads:
            worker.join()

        site.graph_urls = url_manager.urls
        site.graph_connections = url_manager.connections
        site.save()

    def _build_worker_pool(self, que, url_manager, site):
        workers = []
        for _ in range(self.WORKER_POOL_SIZE):
            worker = UrlLoaderTask(que, url_manager, site, self._coord)
            worker.start()
            workers.append(worker)
        return workers
