from ferris import Controller
from google.appengine.api import urlfetch
import json

class Activities(Controller):

    def list(self):
        userid = self.request.params['q']
        if userid:
            self.context['activities'] = self.dump_activities(userid)

    def dump_activities(self, userid):
        url = 'https://www.googleapis.com/plus/v1/people/userid/activities/public?maxResults=100&key=API_KEY'
        API_KEY = 'AIzaSyCpilljYJpgy7k2D1Vbp5zcAIb8EAdoT6U'

        url = url.replace('userid', userid)
        url = url.replace('API_KEY', API_KEY)

        result = urlfetch.fetch(url, validate_certificate=False)

        if result.status_code == 200:
            return result.content.encode('utf-8')
            data = json.loads(result.content, 'utf-8')
            return data['items']
