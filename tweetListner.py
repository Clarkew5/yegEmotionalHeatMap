import tweepy
import configparser
import sys
import json
from collections import deque
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

access_token = "ACCESS TOKEN NOT SET"
access_token_secret = "ACCESS TOKEN SECRET NOT SET"
consumer_key = "CONSUMER KEY NOT SET"
consumer_secret = "CONSUMER SECERET NOT SET"

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.set_autoscaley_on(True)

x = []
ypos = []
yneg = []
yneut = []

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

def animate(i):
    ax1.clear()
    ax1.plot(x, ypos, 'g', x, yneg, 'r', x, yneut, 'k')

class StdOutListener(tweepy.StreamListener):
    numOfTweets = 0
    places = {}
    Canada = {'numPos':0, 'numNeg':0, 'numNeut':0, 'queue':deque(),}

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.ion()

    def on_data(self, data):
        j = json.loads(data)
        if j['place']['country'] != 'Canada':
            return
        place = j['place']['full_name']

        if (place in self.places) == False:
            self.places[place] = {'numPos':0, 'numNeg':0, 'numNeut':0, 'queue':deque(),}

        if len(self.places[place]['queue']) >= 100:
            removedElement = places[place]['queue'].pop()
            if removedElement == 1:
                self.places[place]['numPos'] -= 1
            elif removedElement == -1:
                self.places[place]['numNeg'] -= 1
            elif removedElement == 0:
                self.places[place]['numNeut'] -= 1

        if len(self.Canada['queue']) >= 100:
            removedElement = self.Canada['queue'].pop()
            if removedElement == 1:
                self.Canada['numPos'] -= 1
            elif removedElement == -1:
                self.Canada['numNeg'] -= 1
            elif removedElement == 0:
                self.Canada['numNeut'] -= 1

        sentiment = TextBlob(j['text']).sentiment.polarity
        if sentiment > 0.33:
            self.places[place]['numPos'] += 1
            self.places[place]['queue'].append(1)
            self.Canada['numPos'] += 1
            self.Canada['queue'].append(1)
        elif sentiment < -0.33:
            self.places[place]['numNeg'] += 1
            self.places[place]['queue'].append(-1)
            self.Canada['numNeg'] += 1
            self.Canada['queue'].append(-1)
        elif sentiment <= 0.33 and sentiment >= -0.33:
            self.places[place]['numNeut'] += 1
            self.places[place]['queue'].append(0)
            self.Canada['numNeut'] += 1
            self.Canada['queue'].append(0)
        print(place, ":", "+:", self.places[place]['numPos'], "-:", self.places[place]['numNeg'], "0:", self.places[place]['numNeut'])
        print("CANADA:", "+:", self.Canada['numPos'], "-:", self.Canada['numNeg'], "0:", self.Canada['numNeut'], "len:", len(self.Canada['queue']))
        print("")
        self.numOfTweets += 1

        if len(x) >= 100:
            x.pop(0)
        x.append(self.numOfTweets)

        if len(ypos) >= 100:
            ypos.pop(0)
        ypos.append(self.Canada['numPos'])

        if len(yneg) >= 100:
            yneg.pop(0)
        yneg.append(self.Canada['numNeg'])
        
        if len(yneut) >= 100:
            yneut.pop(0)
        yneut.append(self.Canada['numNeut'])
        print(x)
        ax1.relim()
        ax1.autoscale_view(True,True,True)
        plt.draw()
        plt.pause(0.01)

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
        stream.filter(locations=[-141.561094, 41.676329, -51.053519, 89.9999])
