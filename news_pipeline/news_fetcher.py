# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common_utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://vlagvbqp:zH8auLJC7sn8neTLOCiTdbvd6oO1r-TI@elephant.rmq.cloudamqp.com/vlagvbqp"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news-recommendation-scrape-news-task-queue"

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://vlagvbqp:zH8auLJC7sn8neTLOCiTdbvd6oO1r-TI@elephant.rmq.cloudamqp.com/vlagvbqp"
DEDUPE_NEWS_TASK_QUEUE_NAME = "news-recommendation-dedupe-news-task-queue"


SLEEP_TIME_IN_SECONDS = 5

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
	if msg is None or not isinstance(msg, dict):
		print 'message is broken'
		return

	task = msg

	article = Article(task['url'])
	article.download()
	article.parse()

	task['text'] = article.text

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

	