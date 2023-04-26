import time
from celery_tasks.celery import cel

@cel.task
def send_msg(name):
    print(f'完成向{name}发送短信的任务')
    time.sleep(5)
    return '短信完成'