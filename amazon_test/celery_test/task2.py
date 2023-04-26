import time
from celery_test import app


@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y