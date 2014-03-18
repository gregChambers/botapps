INSTRUCTIONS
============

Install the following libraries:
sudo apt-get install python-oauth2
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install tweepy

Get a consumer_key and consumer_secrect from Twitter:
1- Go to https://dev.twitter.com/apps/new and log in, if necessary
2- Supply the necessary required fields, accept the TOS, and solve the CAPTCHA.
3- Submit the form
4- Copy the consumer key (API key) and consumer secret from the screen into the twitterer.py 
	4.1- consumer_key = 'YOUR_CONSUMER_KEY'
			 consumer_secret = 'YOUR_CONSUMER_SECRET'

Copy twitterer.py script into your raspberrPi, e.g. in /home/pi

Launch the script, e.g. python /home/pi/twitterer.py

Follow the link indicated by the script, sign in and authenticate. Copy the given code into the terminal again.

Now the script will be listening to tweets containing the hashtag indicated in the script. The robot will say every new tweet he detects.

Enjoy!
