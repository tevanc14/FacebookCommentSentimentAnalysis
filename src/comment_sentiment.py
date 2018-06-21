import json
import time

from src.sentiment_analysis import SentimentAnalysis
from src.util import write_local_json, read_local_json


class CommentSentiment:
    def __init__(self, post_comments):
        self.sentiment_analysis = SentimentAnalysis()
        self.post_comments = post_comments

    def get_sentiment_analysis(self, fresh_data):
        """Retrieve sentiment analysis data.

        :param fresh_data: Hit GCP API or read local data
        :returns: Sentiment analysis data for all comments

        """

        if fresh_data:
            self.get_fresh_sentiment_data()

        return read_local_json('sentiments')

    def get_fresh_sentiment_data(self):
        """Get data and write to json file."""

        sentiment_data = self.gather_sentiment_data()
        write_local_json('sentiments', json.loads(json.dumps(sentiment_data)))

    def gather_sentiment_data(self):
        """Iterate through comments to add sentiment data.

        :returns: Dicts of sentiment data

        """

        sentiment_data = []
        for post in self.post_comments:
            datum = {}
            datum['comments'] = []

            if 'message' in post:
                datum['post'] = post['message']

            for comment in post['comments']:
                datum['comments'].append(
                    self.build_sentiment_dictionary(comment['message']))
            sentiment_data.append(datum)

        return sentiment_data

    def build_sentiment_dictionary(self, text):
        """Add the sentiment data to comment.

        :param text: Text of a comment
        :returns: Comment text and sentiment data

        """
        # Manual throttling in case of speedy network
        # time.sleep(1)

        sentiment_object = {}
        sentiment_object['text'] = text
        sentiment_object[
            'textSentiment'] = self.sentiment_analysis.sentiment_text(text)
        entity_sentiment_result = self.sentiment_analysis.entity_sentiment_text(
            text)
        if entity_sentiment_result is not None:
            sentiment_object['entitySentiment'] = entity_sentiment_result
        return sentiment_object
