import os
import pandas as pd

from src.fbdata import FacebookData
from src.comment_sentiment import CommentSentiment
from src.spreadsheet_interaction.write_sentiment import SentimentWriter
from src.spreadsheet_interaction.write_contains_keyword import ContainsKeywordWriter


def get_spreadsheets_of_sentiment():
    """Get Facebook data with sentiment analysis in a spreadsheet."""

    # Gather post and comment data from Facebook Graph API
    facebook_data = FacebookData()
    post_comments = facebook_data.get_post_comments(False)

    # Get sentiment analysis data on comments
    comment_sentiment = CommentSentiment(post_comments)
    sentiment_analysis = comment_sentiment.get_sentiment_analysis(False)

    # Create spreadsheet with comments, sentiment scores, and parent post
    sentiment_writer = SentimentWriter()
    sentiment_writer.write_sentiment_data(sentiment_analysis)

    # Create spreadsheet with comments containing a keyword
    contains_keyword_writer = ContainsKeywordWriter('tax')
    contains_keyword_writer.write_data_that_contains_keyword(post_comments)


if __name__ == '__main__':
    get_spreadsheets_of_sentiment()
