import json
import os

from src.data_interaction import get_post_comments
from src.gcp_nlp import entity_sentiment_text, sentiment_text


def get_sentiment_analysis(fresh_data, post_comments):
    if fresh_data:
        get_sentiment_data(post_comments)

    with open(os.path.join('data', 'sentiments.json'), 'r') as sentiments_file:
        return json.load(sentiments_file)


def get_sentiment_data(post_comments):
    sentiment_data = gather_sentiment_data(post_comments)
    write_sentiment_data(json.loads(json.dumps(sentiment_data)))


def gather_sentiment_data(post_comments):
    sentiment_data = []
    for post in post_comments:
        datum = {}
        datum['comments'] = []

        if 'message' in post:
            datum['post'] = post['message']

        for comment in post['comments']:
            datum['comments'].append(
                build_sentiment_object(comment['message']))
        sentiment_data.append(datum)

    return sentiment_data


def build_sentiment_object(text):
    sentiment_object = {}
    sentiment_object['text'] = text
    sentiment_object['textSentiment'] = sentiment_text(text)
    entity_sentiment_result = entity_sentiment_text(text)
    if entity_sentiment_result is not None:
        sentiment_object['entitySentiment'] = entity_sentiment_result
    return sentiment_object


def write_sentiment_data(sentiment_data):
    with open(os.path.join('data', 'sentiments.json'), 'w') as sentiments_file:
        json.dump(sentiment_data, sentiments_file)
