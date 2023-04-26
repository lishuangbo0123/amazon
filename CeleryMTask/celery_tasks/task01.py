import time
from celery_tasks.celery import cel

@cel.task
def send_email(name):
    print(f'完成向{name}发送邮件的任务')
    time.sleep(5)
    return '邮件'