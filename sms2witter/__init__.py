# Imports
import logging
import os
import re
import sys


import yaml
import twitter
from flask import Flask
from flask import request
app = Flask(__name__)




class TwitterHandler(object):
    """Add keywords to messages and post them to twitter."""
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('TwitterHandler')
        self.api = twitter.Api(
            consumer_key=self.config['consumer_key'],
            consumer_secret=self.config['consumer_secret'],
            access_token_key=self.config['access_token_key'],
            access_token_secret=self.config['access_token_secret'])

    def add_keywords(self, message):
        """Add keywords to message, truncate first if necessary."""
        # Messages may already contain some keywords, so create a list
        # of keywords that this message does not contain.
        keywords_to_add = [keyword for keyword in self.config['keywords']
                if keyword not in message]

        # join keywords with space as seperator
        keyword_str = " ".join(keywords_to_add)

        # remove trailing space form message
        message = re.sub(" $","", message)

        # truncate message to 140 characters minus the length of keywords to
        # append. 
        truncated_message = message[:140-len(keyword_str)]

        # combine truncated message with keywords and return
        message_with_keywords = "%s %s" % (truncated_message, keyword_str)

        # remove any double spaces
        message_with_keywords = re.sub("  *"," ", message_with_keywords)

        logger.debug(
            "Add Keywords: %s + %s --> %s " % (message,
                                               ",".join(keywords_to_add),
                                               message_with_keywords))
        return message_with_keywords

    def _tweet(self, message):
        """Post to twitter"""
        self.api.PostUpdate(message)

    def tweet(self, message):
        """Add keywords, then post to twitter"""
        self._tweet(self.add_keywords(message))


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

config = yaml.load(
    open(os.environ.get('SMS2TWITTER_CONFIG_FILE')))

th = TwitterHandler(config['twitter'])

@app.route("/incomingsms",methods=['GET','POST'])
def hello():
    th.tweet(request.form['smsmessage'])
    return "OK"

if __name__ == "__main__":
    app.debug = True
    app.run()
