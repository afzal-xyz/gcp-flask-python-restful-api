# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Endpoints sample application.

Demonstrates how to create a simple REST API as well as how to secure it using
Google Cloud Endpoints.
"""
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

tasks = {}

TASKS = {
    'task1': {'task': 'create google cloud account'},
    'task2': {'task': 'deploy app in app egnine'},
    'task3': {'task': 'test rest api'},
}


def abort_if_task_doesnt_exist(task_id):
    if task_id not in TASKS:
        abort(404, message="Task {} doesn't exist".format(task_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Task
# shows a single task item and lets you delete a task item
class Task(Resource):
    def get(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        return TASKS[task_id]

    def delete(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        del TASKS[task_id]
        return '', 204

    def put(self, task_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TASKS[task_id] = task
        return task, 201


# TaskList
# shows a list of all tasks, and lets you POST to add new tasks
class TaskList(Resource):
    def get(self):
        return TASKS

    def post(self):
        args = parser.parse_args()
        task_id = int(max(TASKS.keys()).lstrip('task')) + 1
        task_id = 'task%i' % task_id
        TASKS[task_id] = {'task': args['task']}
        return TASKS[task_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/tasks/<task_id>')

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
