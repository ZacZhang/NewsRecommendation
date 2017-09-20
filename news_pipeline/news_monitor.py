# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import redis
import sys

# import common dir in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client
from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://oqocjgvc:wpDedI_G0-d_Tak-ZD35ObDlMrvr97bO@wombat.rmq.cloudamqp.com/oqocjgvc"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news-recommendation-scrape-news-task-queue"
SLEEP_TIME_IN_SECONDS = 10

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
	news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

	num_of_new_news = 0

	for news in news_list:
		news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

		if redis_client.get(news_digest) is None:
			num_of_new_news = num_of_new_news + 1
			news['digest'] = news_digest

			if news['publishedAt'] is None:
				# format: YYYY-MM-DDTHH:MM:SS in UTC
				news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

		redis_client.set(news_digest, news)
		redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

		cloudAMQP_client.sendMessage(news)

	print "Fetched %d new news." % num_of_new_news

	# call news api every 10 seconds
	cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
