from aiohttp import ClientSession
import asyncio


IN_ENDPOINT = 'https://2captcha.com/in.php'
RES_ENDPOINT = 'https://2captcha.com/res.php'


async def twocaptcha_hcaptcha_solve(api_key, site, sitekey, proxy=None):    
    request_params = {
        'key': api_key,
        'method': 'hcaptcha',
        'sitekey': sitekey,
        'json': '1',
        'proxy': proxy if proxy else '',
        'pageurl': site
    }
    solution_id = await _get_solution_id(request_params)
    return solution_id


async def twocaptcha_recaptcha_solve(api_key, sitekey, site, proxy=None):
    request_params = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': sitekey,
        'json': '1',
        'proxy': proxy if proxy else '',
        'pageurl': site
    }
    solution_id = await _get_solution_id(request_params)
    return solution_id


async def twocaptcha_recaptcha_v3_solve(api_key, sitekey, site, action, min_score, proxy=None):
    request_params = {
        'key': api_key,
        'method': 'userrecaptcha',
        'version': 'v3',
        'min_score': min_score,
        'action': action,
        'googlekey': sitekey,
        'json': '1',
        'proxy': proxy if proxy else '',
        'pageurl': site
    }
    solution_id = await _get_solution_id(request_params)
    return solution_id
    

async def _get_solution_id(request_params):
    async with ClientSession() as session:
        async with session.post(IN_ENDPOINT, params=request_params) as r:
            if (await r.json())['status'] == 1:
                solution_id = (await r.json())['request']
            else:
                print(await r.json())
                return 400

    # await asyncio.sleep(15)
    return solution_id


async def get_solution(api_key, solution_id):
    params = {
        'key': api_key,
        'action': 'get',
        'id': solution_id,
        'json': '1'
    }

    async with ClientSession() as session:
        solution = 'CAPCHA_NOT_READY'
        while solution == 'CAPCHA_NOT_READY':
            await asyncio.sleep(5)
            print('TwoCaptcha: ' + str(solution))
            async with session.get(RES_ENDPOINT, params=params) as r:
                solution = (await r.json())['request']
    
    return [solution, 'twocaptcha']
