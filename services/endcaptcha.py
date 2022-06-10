import json

import aiohttp
import asyncio

UPLOAD = 'http://api.endcaptcha.com/upload'
POLL = 'http://api.endcaptcha.com/poll/'


async def endcaptcha_recaptcha_solve(username, password, site, sitekey):
    token_params = {
        'googlekey': sitekey,
        'pageurl': site
    }
    data = {
        'username': username,
        'password': password,
        'type': 4,
        'token_params': json.dumps(token_params)
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(UPLOAD, data=data) as resp:
            print('Endcaptcha: ' + str(await resp.text()))
            try:
                solution_id = (await resp.text()).split('/')[2]
                return solution_id
            except Exception as e:
                print(await resp.text())
                return 400


async def endcaptcha_get_solution(solution_id):
    async with aiohttp.ClientSession() as session:
        status = 'UNSOLVED_YET'
        while status == 'UNSOLVED_YET':
            await asyncio.sleep(3)
            async with session.get(POLL + str(solution_id)) as resp:
                result = await resp.text()
                status = (await resp.text())[:12]
                print('Endcaptcha: ' + str(status))
        return [result, 'endcaptcha']
