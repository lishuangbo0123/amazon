BROKER_URL = 'redis://:@106.13.1.144:6379/1'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://:@106.13.1.144:6379/2'  # 指定 Backend

CELERY_TIMEZONE = 'Asia/Shanghai'                   # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'celery_test.task1',
    'celery_test.task2'
)