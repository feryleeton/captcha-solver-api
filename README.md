# Flask API
## Quick start

### Before runing
- make shure that Redis server installed and running
     ```
     $ sudo systemctl status redis
     $ redis-cli ping
    PONG
    ```
- install requirements

### How to run
- run celery worker
    ```
    celery -A app.celery worker
    ```
- run the script
    ```
    python3 app.py
    ```

### Requests example:
- launch solution for hCaptcha
    ```
    {
        "sitekey": "51829642-2cda-4b09-896c-594f89d700cc",
        "method": "hcaptcha",
        "pageurl": "http://democaptcha.com/demo-form-eng/hcaptcha.html",
        "soft_id": 2834,
        "key": "apikey123",
        "service": "",
        "header_acao": 1,
        "json": 1
    }
    ```
- launch solution for reCaptcha v2
    ```
    {
    "method": "userrecaptcha",
    "version": "v2",
    "pageurl": "https://www.i13websolution.com/wp-test/my-account/",
    "soft_id": 155,
    "googlekey": "6LdglHEUAAAAANl2LgW9XDvFJ6o_qzHzM59y7N8e",
    "key": "apikey123",
    "service": "",
    "header_acao": 1,
    "json": 1
    }  
    ```
- launch solution for reCaptcha v3
    ```
   {
    "version": "v3",
    "action": "examples/v3scores",
    "method": "userrecaptcha",
    "pageurl": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
    "min_score": 0.5,
    "soft_id": 2834,
    "googlekey": "6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696",
    "key": "apikey123",
    "service": "twocaptcha",
    "header_acao": 1,
    "json": 1
    }
    ```
    
- check solution
    ```
   {
    "id": 71584548
    }
    ```
