class BaseTask(object):
    method = None

    def serialize(self, **result):
        result["method"] = self.method
        return result


class HCaptchaTask(BaseTask):
    def __init__(self, website_key, website_url):
        self.method = 'hcaptcha'
        self.website_key = website_key
        self.website_url = website_url

    def serialize(self, **result):
        data = super(HCaptchaTask, self).serialize(**result)
        data["pageurl"] = self.website_url
        data["sitekey"] = self.website_key
        data["method"] = self.method
        return data


class ReCaptchaV2Task(BaseTask):
    def __init__(self, website_key, website_url):
        self.method = 'userrecaptcha'
        self.type = 'v2'
        self.website_key = website_key
        self.website_url = website_url

    def serialize(self, **result):
        data = super(ReCaptchaV2Task, self).serialize(**result)
        data["pageurl"] = self.website_url
        data["googlekey"] = self.website_key
        data["method"] = self.method
        data["version"] = self.type
        return data


class ReCaptchaV3Task(BaseTask):
    def __init__(self, website_key, website_url, min_score, page_action):
        self.method = 'userrecaptcha'
        self.type = 'v3'
        self.website_key = website_key
        self.website_url = website_url
        self.min_score = min_score
        self.page_action = page_action

    def serialize(self, **result):
        data = super(ReCaptchaV3Task, self).serialize(**result)
        data["pageurl"] = self.website_url
        data["googlekey"] = self.website_key
        data["method"] = self.method
        data["version"] = self.type
        data["action"] = self.page_action
        data["min_score"] = self.min_score
        return data
