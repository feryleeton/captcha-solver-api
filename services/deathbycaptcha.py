import json

import aiohttp
import asyncio

SUBMIT_CAPTCHA = 'http://api.dbcapi.me/api/captcha'


async def deathbycaptcha_hcaptcha_solve(username, password, site, sitekey):
    hcaptcha_params = {
        'sitekey': sitekey,
        'pageurl': site
    }
    data = {
        'username': username,
        'password': password,
        'type': 7,
        'hcaptcha_params': json.dumps(hcaptcha_params),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_CAPTCHA, data=data) as resp:
            print('DbcAPI: ' + str(await resp.text()))
            try:
                response = (await resp.text()).split('&')
                for part in response:
                    if 'captcha=' in part:
                        solution_id = part.replace('captcha=', '')
                return solution_id
            except Exception as e:
                print(e)
                return 400


async def deathbycaptcha_recaptcha_solve(username, password, site, sitekey, action='example/action', min_score=0.5):
    token_params = {
        'googlekey': sitekey,
        'pageurl': site,
        'action': action,
        'min_score': min_score
    }
    data = {
        'username': username,
        'password': password,
        'type': 5,
        'token_params': json.dumps(token_params),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_CAPTCHA, data=data) as resp:
            print('DbcAPI: ' + str(await resp.text()))
            try:
                response = (await resp.text()).split('&')
                for part in response:
                    if 'captcha=' in part:
                        solution_id = part.replace('captcha=', '')
                return solution_id
            except Exception as e:
                print(e)
                return 400


async def deathbycaptcha_get_solution(solution_id):
    async with aiohttp.ClientSession() as session:
        result = ''
        while result == '':
            await asyncio.sleep(5)
            async with session.get(SUBMIT_CAPTCHA + '/' + str(solution_id)) as resp:
                response = (await resp.text()).split('&')
                for part in response:
                    if 'text=' in part:
                        result = part.replace('text=', '')
                print('DbcAPI: Pending')
        return [result, 'DbcAPI']
