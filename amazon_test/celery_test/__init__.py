from celery import Celery
app = Celery('amazon')                                # 生成实例
app.config_from_object('celery_test.celeryconfig')   # 加载配置