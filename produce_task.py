from celery_tasks.task01 import send_email
from celery_tasks.task02 import send_msg


result = send_email.delay('yuan')
print(result.id)
result = send_msg.delay('alex')
print(result.id)