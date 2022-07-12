import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'x@S1jJ~6$@yZZ7jeFyU1h7p}Db8jpM55fCeH~BMYaLAA|cV5L26xjQ%HgiQn15dP'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = "info"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or 'sqlite:////home/wuliw/code/tasks_book/data/my_db.db'
