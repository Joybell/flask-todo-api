#-*-coding: utf-8-*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime
import service

apiVersion = 'v1'

app = Flask(__name__)
api = Api(app)

class Tasks(Resource):
    def __init__(self):
        self.service = service.Tasks()

    # Get active tasks
    def get(self):
        try:
            result = self.service.get_active_tasks()
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

    # Create a new task
    def post(self):
        try:
            body = request.get_json()
            result = self.service.create_task(body['task_title'])
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}            

class Task(Resource):
    def __init__(self):
        self.service = service.Tasks()

    # Get an active tasks
    def get(self, task_id):
        try:
            result = self.service.get_active_task(task_id)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

    # Upate a task
    def put(self, task_id):
        try:
            body = request.get_json()
            result = self.service.update_task(task_id, body['task_title'])
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

    # Delete a task
    def delete(self, task_id):
        try:
            result = self.service.delete_task(task_id)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

class TaskStatus(Resource):
    def __init__(self):
        self.service = service.Tasks()

    def post(self, task_id, status):
        try:
            if status == 'close':
                task_status = 'closed'
            elif status == 'reopen':
                task_status = 'active'

            result = self.service.update_task_status(task_id, task_status)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)} 


api.add_resource(Tasks, '/rest/' + apiVersion + '/tasks')
api.add_resource(Task, '/rest/' + apiVersion + '/tasks/<int:task_id>')
api.add_resource(TaskStatus, '/rest/' + apiVersion + '/tasks/<int:task_id>/<string:status>')

if __name__ == '__main__':
    app.run(debug=True)
