# -*- coding: utf-8 -*-
#######################################################################
###   Config.py:     Configuration file for Save Tweets             ###
###   Copyright:     Elena Daehnhardt                               ###
###   Contact me at: edaehn@gmail.com                               ###
#######################################################################
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

########### Importing the necessary methods and libraries ##############
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy.streaming import Stream
import urllib
import os
import time
import signal
import codecs
import json
from datetime import date
import sys
import csv
from config import *

global tweets_added
tweets_added=0




############ Loading the Classification model ##########################
basedir = os.path.abspath(os.path.dirname(__file__))
models_dir = os.path.join(basedir, 'models/')
models_subdirs=[models_dir+s for s in os.listdir(models_dir) if os.path.isdir(models_dir+s)]
MODEL=max(models_subdirs, key=os.path.getmtime)
MODEL=MODEL.rsplit('/', 1)[-1]
if PRINT_DEBUG: print "MODEL=%s"%MODEL
import Classifier
from Locality import getDimension

from sklearn.externals import joblib
c2=Classifier.Classifier() 
filename='./models/'+MODEL+'/META'
try:
	c2 = joblib.load(filename)	
except:
	pass


############ Creating output directories if needed
for dir_is_needed, directory in zip([SAFE_CSV, SAFE_JSON],['./output/csv/','./output/json/']):
	if dir_is_needed and not os.path.exists(directory):
		os.makedirs(directory)	

############ Checking if CSV output files exist, otherwise we create it with headers
if SAFE_CSV:
	csv_output_file='./output/csv/twitter_'+date.today().strftime("%Y-%m-%d")+'.csv'
	if not(os.path.exists(csv_output_file) and os.path.isfile(csv_output_file)):
		with open(csv_output_file, 'a') as f:
			wr=csv.writer(f, dialect='excel')
			header=['Created At', 'User Id', 'User Language', 'User timezone',
				'User Location', 'User Place Country Code from Twitter',
				'User URL', 'User Description', 'User name', 'Tweet',
				'Inferred Country', 'Inferred Dimension', 'Inference Strength',
				'Ratio of Followers', 'Hashtags', 'User Mentions', 'URLs', 'Media'] 
			wr.writerow(header)

############################## Catching Ctrl+C ##########################
def signal_handler(signal, frame):
	try: # we could also do commit here if using DB
		global tweets_added 
		if PRINT_DEBUG:
			print('You pressed Ctrl+C or Killed the process. Your data were saved to DB.')
			print "Tweets added: %s"%str(tweets_added)
	except:
		if PRINT_DEBUG: print('Exception while saving the results in signal_handler.')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
print('Press Ctrl+C to stop the data collection. See the JSON or CSV files in the related /output directories')



############################## Listening to the Twitter Stream ##########################
class StdOutListener(StreamListener):

    def on_data(self, data):
    	global tweets_added
        try:
        	tweet = json.loads(data)
        	if SAFE_JSON:
        		with open('./output/json/twitter_'+date.today().strftime("%Y-%m-%d")+'.txt', 'a') as f:
  					json.dump(data, f, ensure_ascii=False)
	    	tweets_added+=1
	    	self.on_status(tweet)

  
        except BaseException as e:
            if PRINT_DEBUG: print('Failed: ', str(e))
            time.sleep(1)

			
    def on_error(self, status):
        if PRINT_DEBUG: print('Error: ', status)

    def on_status(self, status):


		tweet=[]
		
		try:
			tweet.append(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
		except:
			tweet.append('')

		try:
			tweet.append(status["user"]["id"])
		except:
			tweet.append('')

		try:
			user_language=status["user"]["lang"]
			tweet.append(user_language)
		except:
			tweet.append('')
			user_language=''

		try:
			user_time_zone=status["user"]["time_zone"].encode("utf-8")
			tweet.append(user_time_zone)
		except:
			tweet.append('')
			user_time_zone=''

		try:
			user_location=status["user"]["location"].encode("utf-8")
			tweet.append(user_location)
		except:
			tweet.append('')
			user_location=""
				
		try:
			user_country_code=status["place"]["country_code"]
			tweet.append(user_country_code)
		except:
			user_country_code=""
			tweet.append(user_country_code)

		try:
			tweet.append(status["user"]["url"])
		except:
			tweet.append('')

		try:
			tweet.append(status["user"]["description"].encode("utf-8"))
		except:
			tweet.append('')

		try:
			tweet.append(status["user"]["name"].encode("utf-8"))
		except:
			tweet.append('')
			
		try:
			tweet.append(status["user"]["screen_name"].encode("utf-8"))
		except:
			tweet.append('')

		try:
			tweet.append(status["text"].encode("utf-8"))
		except:
			tweet.append('')
		
		try:
			meta_text=user_language+' '+user_time_zone+' '+user_location
			inferred_country_meta, inferred_dimension_meta=c2.ClassifyTextToCountryDimension(meta_text)
		except Exception as e:
			if PRINT_DEBUG: print e.message
			inferred_country_meta=inferred_dimension_meta=""

		if PRINT_DEBUG: print "inferred_country_meta=%s, inferred_dimension_meta=%s"%(inferred_country_meta, inferred_dimension_meta)

		try:
			tweet.append(inferred_country_meta)
		except:
			tweet.append('')

		try:
			tweet.append(inferred_dimension_meta)
		except:
			tweet.append('')
		_,strength,_=getDimension(inferred_country_meta,user_language)
		if PRINT_DEBUG: print "Inference strength=%d for inferred_country_meta=%s and user_language=%s"%(strength, inferred_country_meta,user_language)
		tweet.append(strength)
		
		if (int(status['user']['followers_count']+status['user']['friends_count']))>0:
			tweet.append(int(status['user']['followers_count'])/(int(status['user']['friends_count'])+int(status['user']['followers_count'])))
		else:
			tweet.append(0)
		
		if 'hashtags' in status['entities']:
			tweet.append(' '.join([hashtag['text'] for hashtag in status['entities']['hashtags']]))
		else:
			tweet.append('')

		if 'user_mentions' in status['entities']:
			tweet.append(' '.join([user_mention['screen_name'] for user_mention in status['entities']['user_mentions']]))
		else:
			tweet.append('')
		
		if 'urls' in status['entities']:
			tweet.append(' '.join([url['expanded_url'] for url in status['entities']['urls']]))
		else:
			tweet.append('')
	
		if 'media' in status['entities']:
			tweet.append(' '.join([media['media_url'] for media in status['entities']['media']]))   
		else:
			tweet.append('')


		if SAFE_CSV:
			with open(csv_output_file, 'a') as f:
				wr=csv.writer(f, dialect='excel')
				wr.writerow(tweet)

		
		return True

	 
    def on_error(self, status):
        print status



if __name__ == '__main__':
	l = StdOutListener()
	try:
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(oauth_token, oauth_secret)
		api_tl = tweepy.API(auth)
	except Exception as e:
		print type(e)
		print e
		print e.args
	
	while True:
		stream = Stream(auth, l)
	
		try:
			stream.filter(track=STREAM_FILTER)
		except Exception as e:
			if PRINT_DEBUG: 
				print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
				print e
			if str(e)=="420": 
				if PRINT_DEBUG: print "I will sleep for 20 seconds before starting to collect again ..."
				time.sleep(20)
			if PRINT_DEBUG: print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			continue


