import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'

# Configuración de Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Configuración de Flask-Caching
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_REDIS_URL = 'redis://localhost:6379/0'
