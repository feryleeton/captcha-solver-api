from aiohttp import ClientSession
import asyncio

HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json'
}

CREATE_TASK_ENDPOINT = 'https://api.anti-captcha.com/createTask'
GET_TASK_RESULT_ENDPOINT = 'https://api.anti-captcha.com/getTaskResult'


async def anticaptcha_hcaptcha_solve(api_key, site, sitekey):
    data = {
        'clientKey': api_key,
        'task': {
            'type': 'HCaptchaTaskProxyless',
            'websiteURL': site,
            'websiteKey': sitekey
        }
    }
    solution_id = await _get_solution_id(data)
    return solution_id


async def anticaptcha_recaptcha_solve(api_key, site, sitekey):
    data = {
        'clientKey': api_key,
        'task': {
            'type': 'RecaptchaV2TaskProxyless',
            'websiteURL': site,
            'websiteKey': sitekey
        }
    }

    solution_id = await _get_solution_id(data)
    return solution_id


async def anticaptcha_recaptcha_v3_solve(api_key, site, sitekey, action, min_score):
    data = {
        'clientKey': api_key,
        'task': {
            'type': 'RecaptchaV3TaskProxyless',
            'websiteURL': site,
            'websiteKey': sitekey,
            'minScore': 0.3,
            'pageAction': action
        }
    }

    solution_id = await _get_solution_id(data)
    return solution_id


async def _get_solution_id(data):
    async with ClientSession(headers=HEADERS) as session:
        async with session.post(CREATE_TASK_ENDPOINT, json=data) as r:
            if (await r.json())['errorId'] == 0:
                solution_id = (await r.json())['taskId']
            else:
                print(await r.json())
                return 400

    # await asyncio.sleep(5)
    return solution_id


async def get_solution(api_key, solution_id):
    data = {
        'clientKey': api_key,
        'taskId': solution_id
    }

    async with ClientSession(headers=HEADERS) as session:
        status = 'processing'
        while status == 'processing':
            await asyncio.sleep(3)
            async with session.get(GET_TASK_RESULT_ENDPOINT, json=data) as r:
                print('AntiCaptcha: ' + str(status))
                status = (await r.json())['status']
                if status == 'ready':
                    solution = (await r.json())['solution']
    
    return [solution, 'anticaptcha']