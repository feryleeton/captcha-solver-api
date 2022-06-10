from captcha_solver import CaptchasolverClient
from captcha_solver import HCaptchaTask, ReCaptchaV3Task, ReCaptchaV2Task
import logging

if __name__ == '__main__':
    """testing all types by using captcha_solver lib"""

    logging.basicConfig(level=logging.INFO)

    # client obj init
    client = CaptchasolverClient('api_key')

    # creating tasks
    hcaptcha_task = HCaptchaTask(website_key='51829642-2cda-4b09-896c-594f89d700cc', website_url='https://democaptcha.com/demo-form-eng/hcaptcha.html')
    recaptcha_v2_task = ReCaptchaV2Task(website_key='6LdglHEUAAAAANl2LgW9XDvFJ6o_qzHzM59y7N8e', website_url='https://www.i13websolution.com/wp-test/my-account/')
    recaptcha_v3_task = ReCaptchaV3Task(website_key='6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696', website_url='https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php', min_score=0.3, page_action='examples/v3scores')

    # launching tasks
    hcaptcha_job = client.launch(hcaptcha_task, service='anticaptcha')
    recaptcha_v2_job = client.launch(recaptcha_v2_task)
    recaptcha_v3_job = client.launch(recaptcha_v3_task)

    print(hcaptcha_job.check_satus())
    print(hcaptcha_job.check_solution())

    # waiting for solution
    print('hCaptcha solution: \n' + str(hcaptcha_job.pull()))
    print('reCaptcha v2 solution: \n' + str(recaptcha_v2_job.pull()))
    print('reCaptcha v3 solution: \n' + str(recaptcha_v3_job.pull()))

    print(hcaptcha_job.check_satus())
    print(hcaptcha_job.check_solution())
