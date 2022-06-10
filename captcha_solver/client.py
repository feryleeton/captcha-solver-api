import time
import requests
import json
import logging


class Job:
    def __init__(self, client, task_id):
        self.client = client
        self.task_id = task_id

    def check_solution(self):
        data = {
            "id": self.task_id
        }
        resp = requests.get('http://127.0.0.1:5000/solution', params=data)
        resp = json.loads(resp.text)

        request = resp['request']
        return request

    def check_satus(self):
        data = {
            "id": self.task_id
        }
        resp = requests.get('http://127.0.0.1:5000/solution', params=data)
        resp = json.loads(resp.text)

        request = resp['status']
        return request

    def pull(self):

        request = 'CAPCHA_NOT_READY'

        data = {
            "id": self.task_id
        }
        logging.info('Checking job #' + str(self.task_id) + ': ')
        while request == 'CAPCHA_NOT_READY':
            time.sleep(3)
            resp = requests.get('http://127.0.0.1:5000/solution', params=data)
            resp = json.loads(resp.text)
            request = resp['request']
            logging.info(resp['request'])
        return request


class CaptchasolverClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def launch(self, task, service=''):
        data = task.serialize()
        data['service'] = service

        resp = requests.post('http://127.0.0.1:5000/solve', data=data)
        resp = json.loads(resp.text)

        task.task_id = resp['request']

        return Job(client=self, task_id=resp['request'])
