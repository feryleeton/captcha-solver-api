import asyncio
import secrets
import sys

from flask import Flask
from flask import jsonify
from flask import request
import logging

import redis

from flask_celery import make_celery

from services import anticaptcha
from services import twocaptcha
from services import imagetyperz
from services import bestcaptchasolver
from services import azcaptcha
from services import deathbycaptcha
from services import endcaptcha

# app configuration
app = Flask(__name__)
app.config.from_object('config.Config')

celery = make_celery(app)
redis_client = redis.Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'], db=0, decode_responses=True)

# logger configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('info.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


async def generate_unique_id():
    # generating random request key for tracking request
    while True:
        request_id = ''.join(str(secrets.choice(range(1, 9))) for i in range(8))
        data = redis_client.hgetall(request_id)
        if data:
            continue
        else:
            break
    return request_id


@celery.task(name="launch_solution")
def launch_solution(anticaptcha_solution_id, twocaptcha_solution_id, imagetyperz_solution_id, bcsapi_solution_id,
                    azcaptcha_solution_id, deathbycaptcha_solution_id, endcaptcha_solution_id, request_id):

    # forming tasks for async run
    tasks = []

    # ignoring services, that by any reason filed
    if twocaptcha_solution_id != 400:
        tasks.append(twocaptcha.get_solution(api_key=app.config['TWOCAPTCHA_TOKEN'], solution_id=twocaptcha_solution_id))
    if anticaptcha_solution_id != 400:
        tasks.append(anticaptcha.get_solution(api_key=app.config['ANTICAPTCHA_TOKEN'], solution_id=anticaptcha_solution_id))
    if bcsapi_solution_id != 400:
        tasks.append(bestcaptchasolver.bcsapi_recaptcha_retrieve(api_key=app.config['BCSAPI_TOKEN'], solution_id=bcsapi_solution_id))
    if endcaptcha_solution_id != 400:
        tasks.append(endcaptcha.endcaptcha_get_solution(endcaptcha_solution_id))
    if imagetyperz_solution_id != 400:
        tasks.append(imagetyperz.get_solution(app.config['IMAGETYPERZ_TOKEN'], imagetyperz_solution_id))
    #if azcaptcha_solution_id != 400:
    #    tasks.append(azcaptcha.azcaptcha_retrieve(api_key=app.config['AZCAPTCHA_TOKEN'], solution_id=azcaptcha_solution_id))
    if deathbycaptcha_solution_id != 400:
        tasks.append(deathbycaptcha.deathbycaptcha_get_solution(solution_id=deathbycaptcha_solution_id))

    # getting first completed task from queue
    done, _ = asyncio.run(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
    solution_token, service = done.pop().result()

    if service == 'anticaptcha':
        solution_token = solution_token['gRecaptchaResponse']

    redis_client.hmset(request_id, {'status': 'READY', 'solution': solution_token, 'service': service})
    redis_client.expire(request_id, 120)

    return solution_token


@app.route('/solve', methods=['POST'])
async def solve():
    logger.info('Got /solve [ POST ] request from ip: ' + str(request.remote_addr) + ' Body: ' + str(request.form))

    request_data = request.form
    # request_data = request.get_json()

    pageurl = request_data['pageurl']
    method = request_data['method']

    if 'service' not in request_data or request_data['service'] == '':
        allowed_services = ['anticaptcha', 'twocaptcha', 'imagetyperz', 'bcsapi', 'azcaptcha', 'deathbycaptcha',
                            'endcaptcha']
    else:
        allowed_services = request_data['service'].split(',')

    if method == 'userrecaptcha':

        googlekey = request_data['googlekey']
        if 'version' in request_data:
            version = request_data['version']
        else:
            version = 'v2'

        if version != 'v3':
            anticaptcha_solution_id = await anticaptcha.anticaptcha_recaptcha_solve(
                api_key=app.config['ANTICAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey
            ) if 'anticaptcha' in allowed_services else 400
            twocaptcha_solution_id = await twocaptcha.twocaptcha_recaptcha_solve(
                api_key=app.config['TWOCAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey
            ) if 'twocaptcha' in allowed_services else 400
            imagetyperz_solution_id = await imagetyperz.imagetyperz_recaptcha_solve(
                api_key=app.config['IMAGETYPERZ_TOKEN'],
                site=pageurl,
                sitekey=googlekey
            ) if 'imagetyperz' in allowed_services else 400
            bcsapi_solution_id = await bestcaptchasolver.bcsapi_recaptcha_solve(
                api_key=app.config['BCSAPI_TOKEN'],
                site=pageurl,
                sitekey=googlekey
            ) if 'bcsapi' in allowed_services else 400
            azcaptcha_solution_id = await azcaptcha.azcaptcha_recaptcha_solve(
                api_key=app.config['AZCAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey
            ) if 'azcaptcha' in allowed_services else 400
            deathbycaptcha_solution_id = await deathbycaptcha.deathbycaptcha_recaptcha_solve(
                username=app.config['DEATHBYCAPTCHA_LOGIN'],
                password=app.config['DEATHBYCAPTCHA_PASSWORD'],
                site=pageurl,
                sitekey=googlekey
            ) if 'deathbycaptcha' in allowed_services else 400
            endcaptcha_solution_id = await endcaptcha.endcaptcha_recaptcha_solve(
                username=app.config['ENDCAPTCHA_LOGIN'],
                password=app.config['ENDCAPTCHA_PASSWORD'],
                site=pageurl,
                sitekey=googlekey
            ) if 'endcaptcha' in allowed_services else 400
        else:
            action = request_data['action']
            min_score = request_data['min_score']
            anticaptcha_solution_id = await anticaptcha.anticaptcha_recaptcha_v3_solve(
                api_key=app.config['ANTICAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey,
                action=action,
                min_score=min_score
            ) if 'anticaptcha' in allowed_services else 400
            twocaptcha_solution_id = await twocaptcha.twocaptcha_recaptcha_v3_solve(
                api_key=app.config['TWOCAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey,
                action=action,
                min_score=min_score
            ) if 'twocaptcha' in allowed_services else 400

            # ReCaptcha v3 is not supported
            imagetyperz_solution_id = 400

            bcsapi_solution_id = await bestcaptchasolver.bcsapi_recaptcha_v3_solve(
                api_key=app.config['BCSAPI_TOKEN'],
                site=pageurl,
                sitekey=googlekey,
                action=action,
                min_score=min_score
            ) if 'bcsapi' in allowed_services else 400
            azcaptcha_solution_id = await azcaptcha.azcaptcha_recaptcha_v3_solve(
                api_key=app.config['AZCAPTCHA_TOKEN'],
                site=pageurl,
                sitekey=googlekey,
                action=action,
                min_score=min_score
            ) if 'azcaptcha' in allowed_services else 400
            deathbycaptcha_solution_id = await deathbycaptcha.deathbycaptcha_recaptcha_solve(
                username=app.config['DEATHBYCAPTCHA_LOGIN'],
                password=app.config['DEATHBYCAPTCHA_PASSWORD'],
                site=pageurl,
                sitekey=googlekey,
                action=action,
                min_score=min_score
            ) if 'deathbycaptcha' in allowed_services else 400

            # ReCaptcha v3 is not supported
            endcaptcha_solution_id = 400

    elif method == 'hcaptcha':

        sitekey = request_data['sitekey']

        anticaptcha_solution_id = await anticaptcha.anticaptcha_hcaptcha_solve(
            api_key=app.config['ANTICAPTCHA_TOKEN'],
            site=pageurl,
            sitekey=sitekey
        ) if 'anticaptcha' in allowed_services else 400
        twocaptcha_solution_id = await twocaptcha.twocaptcha_hcaptcha_solve(
            api_key=app.config['TWOCAPTCHA_TOKEN'],
            site=pageurl,
            sitekey=sitekey
        ) if 'twocaptcha' in allowed_services else 400
        imagetyperz_solution_id = await imagetyperz.imagetyperz_hcaptcha_solve(
            api_key=app.config['IMAGETYPERZ_TOKEN'],
            site=pageurl,
            sitekey=sitekey
        ) if 'imagetyperz' in allowed_services else 400
        bcsapi_solution_id = await bestcaptchasolver.bcsapi_hcaptcha_solve(
            api_key=app.config['BCSAPI_TOKEN'],
            site=pageurl,
            sitekey=sitekey
        ) if 'bcsapi' in allowed_services else 400
        azcaptcha_solution_id = await azcaptcha.azcaptcha_hcaptcha_solve(
            api_key=app.config['AZCAPTCHA_TOKEN'],
            site=pageurl,
            sitekey=sitekey
        ) if 'azcaptcha' in allowed_services else 400
        deathbycaptcha_solution_id = await deathbycaptcha.deathbycaptcha_hcaptcha_solve(
            username=app.config['DEATHBYCAPTCHA_LOGIN'],
            password=app.config['DEATHBYCAPTCHA_PASSWORD'],
            site=pageurl,
            sitekey=sitekey
        )
        # hCaptcha is not supported
        endcaptcha_solution_id = 400

    request_id = await generate_unique_id()

    result = launch_solution.delay(
        anticaptcha_solution_id=anticaptcha_solution_id,
        twocaptcha_solution_id=twocaptcha_solution_id,
        azcaptcha_solution_id=azcaptcha_solution_id,
        bcsapi_solution_id=bcsapi_solution_id,
        deathbycaptcha_solution_id=deathbycaptcha_solution_id,
        endcaptcha_solution_id=endcaptcha_solution_id,
        imagetyperz_solution_id=imagetyperz_solution_id,
        request_id=request_id
    )

    redis_client.hmset(request_id, {'status': 'PENDING', 'solution': '', 'service': ''})

    return jsonify({"status": 1,
                    "request": request_id
                    })


@app.route('/solution', methods=['GET'])
async def solution():
    """
    Returns the solution or a solving status
    """

    logger.info('Got /solution [ GET ] request from ip: ' + str(request.remote_addr) + ' Body: ' + str(request.args))
    request_id = request.args.get('id')
    #request_data = request.get_json()
    #request_id = request_data['id']

    data = redis_client.hgetall(request_id)

    if not data:
        return jsonify({
            "status": 0,
            "error": "wrong request id"
        })
    else:
        if data['status'] == 'READY':
            solution = data['solution']
            service = data['service']
            return jsonify({
                "status": 1,
                "request": solution,
                "service": service
            })
        else:
            return jsonify({
                "status": 0,
                "request": "CAPCHA_NOT_READY"
            })


if __name__ == '__main__':
    logger.info('App started')
    app.run()
