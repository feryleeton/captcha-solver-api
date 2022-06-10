import json

import aiohttp
import asyncio

IN = 'http://azcaptcha.com/in.php'
RES = 'http://azcaptcha.com/res.php'


async def azcaptcha_recaptcha_solve(api_key, site, sitekey):
    data = {
        'key': api_key,
        'method': 'userrecaptcha',
        'pageurl': site,
        'googlekey': sitekey,
        'json': 1,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(IN, data=data) as resp:
            print('AzCaptcha: ' + str(await resp.text()))
            result = json.loads(await resp.text())
            if result['status'] == 0:
                return 400
            else:
                return result['request']


async def azcaptcha_recaptcha_v3_solve(api_key, site, sitekey, action, min_score):
    data = {
        'key': api_key,
        'method': 'userrecaptcha',
        'pageurl': site,
        'googlekey': sitekey,
        'version': 'v3',
        'min_score': min_score,
        'action': action,
        'json': 1,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(IN, data=data) as resp:
            print('AzCaptcha: ' + str(await resp.text()))
            result = json.loads(await resp.text())
            if result['status'] == 0:
                return 400
            else:
                return result['request']


async def azcaptcha_hcaptcha_solve(api_key, site, sitekey):
    data = {
        'key': api_key,
        'method': 'hcaptcha',
        'pageurl': site,
        'sitekey': sitekey,
        'json': 1,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(IN, data=data) as resp:
            print('AzCaptcha: ' + str(await resp.text()))
            result = json.loads(await resp.text())
            if result['status'] == 0:
                return 400
            else:
                return result['request']


async def azcaptcha_retrieve(api_key, solution_id):
    status = 'CAPCHA_NOT_READY'
    while status == 'CAPCHA_NOT_READY':
        await asyncio.sleep(5)
        print('Azcaptcha: ' + str(status))
        async with aiohttp.ClientSession() as session:
            async with session.get(RES + '?key=' + str(api_key) + '&action=get&id=' + str(solution_id) + '&json=1') as resp:
                status = json.loads(await resp.text())['request']
    return [status, 'azcaptcha']

