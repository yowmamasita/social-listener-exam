from ferris import Controller
import tweepy

class Tweets(Controller):

    def list(self):
        try:
            screen_name = self.request.params['q']
            if screen_name:
                self.context['tweets'] = self.dump_tweets(screen_name)
            else:
                raise KeyError
        except:
            return "Invalid input"

    def dump_tweets(self, screen_name):
        CONSUMER_KEY = 'clITZxFzGKPVAR1jK0MiA'
        CONSUMER_SECRET = 'cgc2dkp8tHnmafMlTX9YNIGC2vGQ0PSHfDEvNrZxDM'
        ACCESS_TOKEN_KEY = '46553004-r8r7tF6e7Ix63XdZpcKkrIpdllnDZ8f02zyrHoaVG'
        ACCESS_TOKEN_SECRET = 'vqqCeTIC8wXb4zFlYI17hN8nsyjbh2KhG8vSZ7vUjF7dc'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        tweets = []
        tweets.extend(new_tweets)

        oldest_id = tweets[-1].id - 1

        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_id)
            tweets.extend(new_tweets)
            oldest_id = tweets[-1].id - 1

        return tweets
