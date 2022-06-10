import json

import aiohttp
import asyncio

HEADERS = {
    'User-Agent': 'pythonAPI1.0'
}

BALANCE_ENDPOINT_TOKEN = 'http://captchatypers.com/Forms/RequestBalanceToken.ashx'
SUBMIT_HCAPTCHA_TOKEN = 'http://www.captchatypers.com/captchaapi/UploadHCaptchaUser.ashx'
SUBMIT_RECAPTCHA_TOKEN = 'http://www.captchatypers.com/captchaapi/UploadRecaptchaToken.ashx'
RES_ENDPOINT = 'http://www.captchatypers.com/captchaapi/GetCaptchaResponseJson.ashx'


async def imagetyperz_hcaptcha_solve(api_key, site, sitekey):

    data = {
        'token': api_key,
        'captchatype': 11,
        'pageurl': site,
        'sitekey': sitekey,
        'action': 'UPLOADCAPTCHA',

    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_HCAPTCHA_TOKEN, data=data) as resp:
            print('Imagetyperz: ' + str(await resp.text()))
            try:
                return json.loads(await resp.text())[0]['CaptchaId']
            except Exception as e:
                print('Imagetyperz: ' + str(e) + ' ignoring service...')
                return 400


async def imagetyperz_recaptcha_solve(api_key, site, sitekey):

    data = {
        'token': api_key,
        'pageurl': site,
        'sitekey': sitekey,
        'action': 'UPLOADCAPTCHA',

    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SUBMIT_HCAPTCHA_TOKEN, data=data) as resp:
            print('Imagetyperz: ' + str(await resp.text()))
            try:
                return json.loads(await resp.text())[0]['CaptchaId']
            except Exception as e:
                print('Imagetyperz: ' + str(e) + ' ignoring service...')
                return 400


async def get_balance(api_key):
    async with aiohttp.ClientSession() as session:
        async with session.post(BALANCE_ENDPOINT_TOKEN, data={'token': api_key, 'action': 'REQUESTBALANCE'}) as resp:
            return json.loads(await resp.text())


async def get_solution(api_key, solution_id):
    data = {
        'token': api_key,
        'captchaID': int(solution_id),
        'action': 'GETTEXT',
    }
    async with aiohttp.ClientSession() as session:
        status = 'Pending'
        while status == 'Pending':
            await asyncio.sleep(5)
            print('Imagetyperz: ' + str(status))
            async with session.post(RES_ENDPOINT,
                                    data=data) as resp:
                solution = await resp.json(content_type=None)
                key = solution[0]['Response']
                status = solution[0]['Status']
        return [key, 'imagetyperz']
