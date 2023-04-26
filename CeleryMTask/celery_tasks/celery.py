from __init__ import Celery
cel = Celery('celery_demo',
             broker = 'redis://:@106.13.1.144:6379/1',
             backend = 'redis://:@106.13.1.144:6379/2',
             include = ['celery_tasks.task01',
                        'celery_tasks.task02'])

#时区
cel.conf.timezone = 'Asia/Shanghai'
#是否使用UTC
cel.conf.enable_utc = False