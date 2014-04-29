#!/usr/bin/env python

# Name: botapp_parrot
# Author: Pablo Garcia, pgarcia@aisoy.com
# License: BSD

import rospy
import roslib; 
roslib.load_manifest('aisoy_sdk_asr')
roslib.load_manifest('aisoy_sdk_tts')
roslib.load_manifest('aisoy_common')
from libaisoy_sdk_asr import *;
from libaisoy_sdk_tts import *;
from libaisoy_common import *

asr = Asr(AsrName.GoogleAsr)
tts = Tts(TtsName.Festival)

if __name__ == '__main__':
	rospy.init_node('botapp_parrot')
	tts.setTtsLanguage(Language.English)
	asr.setAsrLanguage(Language.English)

	asr.startListening()
	tts.say("Hello. This is the parrot botapp. Tell me something and I will repeat it")

	while not rospy.is_shutdown():
		print "Say something..."
		listened = asr.listen()

		if listened:
		  print "Listened: " + listened
		  tts.say(listened)

		if "stop" in listened  or "exit" in listened:
			break

	tts.say("Ok, we have finished. See you later, alligator.")
	asr.stopListening()
