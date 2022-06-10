import json

import aiohttp
import asyncio

HEADERS = {
    'User-Agent': 'pythonAPI1.0'
}

SUBMIT_RECAPTCHA = 'https://bcsapi.xyz/api/captcha/recaptcha'
SUBMIT_HCAPTCHA = 'https://bcsapi.xyz/api/captcha/hcaptcha'
RETRIEVE_CAPTCHA = 'https://bcsapi.xyz/api/captcha/'


async def bcsapi_recaptcha_solve(api_key, site, sitekey):
    data = {
        'access_token': api_key,
        'page_url': site,
        'site_key': sitekey
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_RECAPTCHA, data=data) as resp:
            print('BcsAPI: ' + str(await resp.text()))
            try:
                return json.loads(await resp.text())['id']
            except Exception as e:
                print('BcsAPI: ' + str(e) + ' ignoring service...')
                return 400


async def bcsapi_recaptcha_v3_solve(api_key, site, sitekey, action, min_score):
    data = {
        'access_token': api_key,
        'page_url': site,
        'type': 3,
        'v3_min_score': min_score,
        'site_key': sitekey,
        'v3_action': action
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_RECAPTCHA, data=data) as resp:
            print('BcsAPI: ' + str(await resp.text()))
            try:
                return json.loads(await resp.text())['id']
            except Exception as e:
                print('BcsAPI: ' + str(e) + ' ignoring service...')
                return 400


async def bcsapi_hcaptcha_solve(api_key, site, sitekey):
    data = {
        'access_token': api_key,
        'page_url': site,
        'site_key': sitekey
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_HCAPTCHA, data=data) as resp:
            print('BcsAPI: ' + str(await resp.text()))
            try:
                return json.loads(await resp.text())['id']
            except Exception as e:
                print('BcsAPI: ' + str(e) + ' ignoring service...')
                return 400


async def bcsapi_recaptcha_retrieve(api_key, solution_id):
    async with aiohttp.ClientSession() as session:
        status = 'pending'
        while status == 'pending':
            await asyncio.sleep(6)
            print('BcsAPI: ' + str(status))
            async with session.get(RETRIEVE_CAPTCHA + str(solution_id) + '?access_token=' + str(api_key)) as resp:
                result = json.loads(await resp.text())
                status = result['status']
        try:
            # reCaptcha
            return [result['gresponse'], 'bcsapi']
        except KeyError:
            # hCaptcha
            return [result['solution'], 'bcsapi']