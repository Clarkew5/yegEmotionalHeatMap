import tweepy
import configparser
import sys
import json

access_token = "ACCESS TOKEN NOT SET"
access_token_secret = "ACCESS TOKEN SECRET NOT SET"
consumer_key = "CONSUMER KEY NOT SET"
consumer_secret = "CONSUMER SECERET NOT SET"

def readConfig(FileName):
    config = configparser.ConfigParser()
    config.read(FileName)
    global access_token
    access_token = config['DEFAULT']['access_token']
    global access_token_secret
    access_token_secret = config['DEFAULT']['access_token_secret']
    global consumer_key
    consumer_key = config['DEFAULT']['consumer_key']
    global consumer_secret
    consumer_secret = config['DEFAULT']['consumer_secret']

class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        j = json.loads(data)
        text = j['text']
        print(text)

    def on_error(self, status):
        print('Error: ' + str(status))

if (__name__ == '__main__'):
    if (len(sys.argv) != 2):
        print("Enter in an imput file")
    else:
        readConfig(sys.argv[1])
        listener = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        stream = tweepy.Stream(auth=api.auth, listener=listener)

        stream.filter(locations=[-113.690643, 53.406667, -113.332214, 53.661323])
