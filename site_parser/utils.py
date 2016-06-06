from celery.signals import worker_process_init


@worker_process_init.connect
def fix_multiprocessing(**kwargs):
    from multiprocessing import current_process
    try:
        current_process()._config
    except AttributeError:
        current_process()._config = {'semprefix': '/mp'}