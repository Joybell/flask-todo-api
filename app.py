#-*-coding: utf-8-*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
from flask_cors import CORS, cross_origin
from datetime import datetime
import module.service as service

apiVersion = 'v1'

app = Flask(__name__)
api = Api(app)
CORS(app)

class Tasks(Resource):
    def __init__(self):
        self.service = service.Tasks()

    # Get active/close tasks
    def get(self):
        try:
            task_status = request.args.get('task_status', 'active', type = str)
            task_title = request.args.get('task_title')
            page = request.args.get('page', 1, type = int)
          
            params = dict()
            params['task_status'] = task_status
            params['task_title'] = task_title
            params['page'] = page
            
            result = dict()
            result['recordSet'] = self.service.get_tasks(params)

            if task_status == 'active':
                rows = self.service.get_tasks_count(params)
                result['totalCount'] = rows['totalCount']

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

    # Get a task
    def get(self, task_id):
        try:
            result = self.service.get_task(task_id)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

    # Upate a task
    def put(self, task_id):
        try:
            if request.data:
                req_data = request.get_json()    
                result = self.service.update_task(task_id, req_data['task_title'])
                self.service.update_pre_tasks(task_id, req_data['pre_tasks'])
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

    # Update a task status
    def put(self, task_id, actionStatus):
        try:
            if actionStatus == 'close':
                task_status = 'closed'
                
                result = self.service.get_active_pre_tasks(task_id)
                if len(result) > 0:
                    err = dict()
                    err['result_code'] = 'FAIL'
                    err['message'] = '완료되지 않은 선행 이슈가 존재합니다.'

                    return jsonify(err)
            elif actionStatus == 'reopen':
                task_status = 'active'

            result = self.service.update_task_status(task_id, task_status)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)} 

class PreTasks(Resource):
    def __init__(self):
        self.service = service.Tasks()

    def get(self):
        try:
            result = self.service.get_pre_tasks()
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)} 

api.add_resource(Tasks, '/rest/' + apiVersion + '/tasks')
api.add_resource(Task, '/rest/' + apiVersion + '/task/<int:task_id>')
api.add_resource(TaskStatus, '/rest/' + apiVersion + '/task/<int:task_id>/<string:actionStatus>')
api.add_resource(PreTasks, '/rest/' + apiVersion + '/pre_tasks')

if __name__ == '__main__':
    app.run(debug = True)
