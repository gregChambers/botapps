#!/usr/bin/env python
import time 
import unicodedata 
from Queue import *
import oauth2 as oauth
import tweepy
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl
    
import rospy
import roslib; 
roslib.load_manifest('aisoy_sdk_tts')
roslib.load_manifest('aisoy_common')
from libaisoy_sdk_tts import *;
from libaisoy_common import *

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'

####### TWITTERER CLASS ##################################################
class Twitterer:
    def __init__(self):
        self.authenticate()
        self.HASHTAG="#aisoyrobot"
        self.tts = Tts(TtsName.Festival)
        self.tts.setTtsLanguage(Language.English)

    def authenticate(self):
        # Authentication
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        oauth_client = oauth.Client(oauth_consumer)

        print 'Requesting temp token from Twitter'
        resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

        if resp['status'] != '200':
            print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
        else:
            request_token = dict(parse_qsl(content))
            url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])

            print '\nI will try to start a browser to visit the following Twitter page'
            print 'if a browser will not start, copy the URL to your browser'
            print 'and retrieve the pincode to be used'
            print 'in the next step to obtain an Authentication Token: \n' + url + "\n"

            #webbrowser.open(url)
            pincode = raw_input('Pincode? ')

            token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            token.set_verifier(pincode)

            print '\nGenerating and signing request for an access token\n'

            oauth_client = oauth.Client(oauth_consumer, token)
            resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_callback=oob&oauth_verifier=%s' % pincode)
            access_token = dict(parse_qsl(content))

            if resp['status'] != '200':
                print 'The request for a Token did not succeed: %s' % resp['status']
                print access_token
            else:
                access_token_key = access_token['oauth_token']
                access_token_secret = access_token['oauth_token_secret']
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token_key, access_token_secret)
                self.api = tweepy.API(auth)
                
    def mainLoop(self):
        TIME_TO_WAIT = 5
        NUM_MAX_TWITS = 20
        self.queue = Queue(NUM_MAX_TWITS)
        self.already_said = []
        print "waiting for twitts with hashtag " + str(self.HASHTAG) + "......."
        while not rospy.is_shutdown():
            first = self.is_first_iteration()
            self.search_new_hashtag(NUM_MAX_TWITS)
            while not self.queue.empty():
                last = self.queue.get()
                self.already_said.append(last)
                if not first:
                    self.say(last[0],last[1])
            time.sleep(TIME_TO_WAIT)
            
    def is_first_iteration(self):
        if self.already_said == []:
            return True
        else:
            return False
                
    def search_new_hashtag(self, max_twits):	
        for tweets in self.api.search(q=self.HASHTAG,count=max_twits, result_type='recent'):
            if not self.is_already_said(tweets.user.screen_name,tweets.text):
                self.queue.put((tweets.user.screen_name,tweets.text))
        
    def is_already_said(self, user, msg):
        if (user,msg) in self.already_said:
            return True
        return False

    def removeAccents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        only_ascii = nkfd_form.encode('ASCII', 'ignore')
        return only_ascii

    def say(self, user, msg):
        print "User " +user+" just twitted "+ msg
        to_say = "User " +user+" just twitted"
        self.tts.say(self.removeAccents(to_say))
        to_say = msg.replace(self.HASHTAG,"")
        self.tts.say(self.removeAccents(to_say))

####### MAIN #############################################################
if __name__ == '__main__':
    twitterer = Twitterer()
    rospy.init_node('twitterer_node')
    twitterer.mainLoop()
