from flask_restful import Api

from app import app
from .tasks import task_api


api = Api(app=app)

api.add_resource(task_api, "/api/tasks/")
