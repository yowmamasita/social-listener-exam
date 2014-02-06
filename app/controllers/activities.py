from ferris import Controller

class Activities(Controller):

    def list(self):
        return self.dump_activities('115787402613940736973')

    def dump_activities(self, userid):
        url = 'https://www.googleapis.com/plus/v1/people/userid/activities/public?maxResults=100&key='
        API_KEY = 'AIzaSyCpilljYJpgy7k2D1Vbp5zcAIb8EAdoT6U'

        url.replace('userid', userid)
        url += API_KEY

        return url
