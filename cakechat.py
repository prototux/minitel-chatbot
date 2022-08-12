import requests
import logging

class cakechat:
    def __init__(self, service):
        self.url = service
        self.context = []
        self.logger = logging.getLogger('minitelbot')
        self.mood = 'neutral'
        self.moods = ['neutral', 'joy', 'anger', 'sadness', 'fear']

    def reset(self):
        self.mood = 'neutral'
        self.context = []

    def setMood(self, mood):
        if mood in self.moods:
            self.mood = mood
            return True
        return False

    def send(self, str):
        # Remove earliest sentence from context
        if len(self.context) == 3:
            self.context.pop(0)

        self.context.append(str)

        self.logger.info(f'sending to cakechat with context {self.context}')

        data = {'context': self.context, 'emotion': self.mood}
        resp = requests.post(f'http://{self.url}/cakechat_api/v1/actions/get_response', json=data)
        self.logger.info(f'response from cakechat: {resp.json()}')
        return resp.json().get('response', 'sorry, i didnt understand')
