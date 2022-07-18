from flask import request
from flask_restful import Resource

from logic import db
from logic.models import Task


class task_api(Resource):

    def get(self):
        data_from_db = db.session.query(Task).all()
        out = {}
        
        for item in data_from_db:
            out.update({str(item.id) : item.get_value_task()})
        
        return out


    def post(self):
        
        data_from_request = request.get_json()
        task_new = Task(
            title = data_from_request["title"],
            content = data_from_request["content"]
            )        

        db.session.add(task_new)
        db.session.commit()

        return {
            "title" : "200",
            "info" : task_new.title
        }


    def put(self):
        ts_from_db =  db.session.query(Task).get(int(request.args.get("id")))
        data_from_request = request.get_json()

        if ts_from_db:
            ts_from_db.title = data_from_request["title"]
            ts_from_db.content = data_from_request["content"]

            db.session.add(ts_from_db)
            db.session.commit()

            return {
                "good" : 200
            }
        else:
            return {
                "error" : "invalid id"
            }


    def delete(self):
        ts_from_db =  db.session.query(Task).get(int(request.args.get("id")))
                
        if ts_from_db:
            db.session.delete(ts_from_db)
            db.session.commit()
            return {
                "good" : 200
            }
        else:
            return {
                "error" : "invalid id"
            }