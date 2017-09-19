# -*- coding: utf-8 -*-

import os
import sys

#from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://oqocjgvc:wpDedI_G0-d_Tak-ZD35ObDlMrvr97bO@wombat.rmq.cloudamqp.com/oqocjgvc"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news-recommendation-scrape-news-task-queue"

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://upoxrqsz:sAEuVrTktZhU6r3g1cPUoJMOcJ-i1VlQ@rhino.rmq.cloudamqp.com/upoxrqsz"
DEDUPE_NEWS_TASK_QUEUE_NAME = "news-recommendation-dedupe-news-task-queue"


SLEEP_TIME_IN_SECONDS = 5

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
	if msg is None or not isinstance(msg, dict):
		print 'message is broken'
		return

	task = msg
	text = None

	# We support cnn only now
	if task['source'] == 'cnn':
		print 'Scraping CNN news'
		text = cnn_news_scraper.extract_news(task['url'])
	else:
		print 'News source [%s] is not supported.' % task['source']

	task['text'] = text

	dedupe_news_queue_client.sendMessage(task)


while True:
	# Fetch msg from queue
	if scrape_news_queue_client is not None:
		msg = scrape_news_queue_client.getMessage()
		if msg is not None:
			# Handle msg
			try:
				handle_message(msg)
			except Exception as e:
				print e
				pass
		scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

	