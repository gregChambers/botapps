#!/usr/bin/env python

# Name: botapp_wolfram
# Author: Pablo Garcia, pgarcia@aisoy.com
# License: BSD

import wolframalpha
import sys
import unicodedata 
    
import rospy
import roslib; 
roslib.load_manifest('aisoy_sdk_tts')
roslib.load_manifest('aisoy_sdk_asr')
roslib.load_manifest('aisoy_sdk_translate')
roslib.load_manifest('aisoy_common')
from libaisoy_sdk_tts import *;
from libaisoy_sdk_asr import *;
from libaisoy_sdk_translate import *;
from libaisoy_common import *

#You can get a free API key here http://products.wolframalpha.com/api/
APP_ID='Q59EW4-7K8AHE858R'

LANGUAGE = Language.English #Language.Spanish, Language.French, etc...

####### WOLFRAM CLASS ##################################################
class Wolfram:
	def __init__(self):
		self.client = wolframalpha.Client(APP_ID)
		self.tts = Tts(TtsName.GoogleTts)
		self.tts.setTtsLanguage(LANGUAGE)
		self.asr = Asr(AsrName.GoogleAsr)
		self.asr.setAsrLanguage(LANGUAGE)
		self.translate = Translate()
 
	def mainLoop(self):
		while not rospy.is_shutdown():
			rospy.loginfo("Waiting for user sentence........")
			sentence = self.asr.listen()

			if sentence != "":
				rospy.loginfo("Question: %s",sentence)
				if LANGUAGE != Language.English:
					sentence = self.translate.translate(sentence, LANGUAGE, Language.English)

				answer = self.process_sentence(sentence)

				if LANGUAGE != Language.English:
					answer = self.translate.translate(answer, Language.English, LANGUAGE)

				rospy.loginfo("Answer: %s",answer)
				self.tts.say(answer)

	def process_sentence(self, sentence):
		query = sentence
		res = self.client.query(query)

		if len(res.pods) > 0:
			texts = ""
			pod = res.pods[1]
			if pod.text:
				texts = ". ".join(elem for elem in self.toASCII(pod.text).split("\n"))
				texts = texts.replace("|","")
			else:
			  texts = "I have no answer for that"
			return texts
		else:
			return "I am not sure"

	def toASCII(self, input_str):
		nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
		only_ascii = nkfd_form.encode('ASCII', 'ignore')
		return only_ascii

####### MAIN #############################################################
if __name__ == '__main__':
    wolfram = Wolfram()
    rospy.init_node('wolfram_node')
    wolfram.mainLoop()
