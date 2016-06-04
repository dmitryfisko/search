from __future__ import absolute_import

from time import sleep

from celery import shared_task
from celery._state import current_task


#  /usr/bin/python3.5 manage.py celery -A search worker -l info --concurrency=10
@shared_task
def test(param):
    sleep(5)
    return 'current thread %s' % current_task.request.id
    # return 'The test task executed with argument "%s" ' % param
