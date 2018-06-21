import os
import pandas as pd


class SentimentWriter():
    def __init__(self):
        self.positives = {'post': '', 'text': [], 'score': []}
        self.negatives = {'post': '', 'text': [], 'score': []}
        self.writer = pd.ExcelWriter(os.path.join('output', 'sentiment.xlsx'))

    def write_sentiment_data(self, sentiment_analysis):
        """Write comments and their sentiment score to a spreadsheet.
        
        Arguments:
            sentiment_analysis {list} -- Comments with sentiment information
        """

        for post in sentiment_analysis:
            self.process_post(post)

        self.writer.save()

    def process_post(self, post):
        """Iterate through posts to process their comments.
        
        Arguments:
            post {dict} -- Post with its respective comments
        """

        if 'post' in post:
            self.positives['post'] = post['post']
            self.negatives['post'] = post['post']
            for comment in post['comments']:
                self.process_comment(comment)

            self.write_sentiment_to_excel()

    def process_comment(self, comment):
        """Gather sentiment data from a comment and separate positive from negative.
        
        Arguments:
            comment {dict} -- Comment with sentiment data
        """

        if 'score' in comment['textSentiment']['documentSentiment']:
            if comment['textSentiment']['documentSentiment']['score'] > 0:
                add_comment(comment, self.positives)
            else:
                add_comment(comment, self.negatives)

    def write_sentiment_to_excel(self):
        """Write positive and negative comments to separate sheets."""

        dataframe_positive = pd.DataFrame(data=self.positives)
        dataframe_negative = pd.DataFrame(data=self.negatives)

        dataframe_positive.to_excel(
            self.writer,
            'Positive - ' + get_post_abbreviation(self.positives) + '...')
        dataframe_negative.to_excel(
            self.writer,
            'Negative - ' + get_post_abbreviation(self.negatives) + '...')


def add_comment(comment, comment_container):
    """Add the text and overall sentiment to a container.
    
    Arguments:
        comment {dict} -- Comment with sentiment data
        comment_container {dict} -- Holds comment text, sentiment score, and respective post
    """

    comment_container['text'].append(comment['text'])
    comment_container['score'].append(
        comment['textSentiment']['documentSentiment']['score'])


def get_post_abbreviation(comment_container):
    """Get an abbreviation of the post text to label the corresponding sheet.
    
    Arguments:
        comment_container {dict} -- Holds comment text, sentiment score, and respective post
    
    Returns:
        [string] -- Abbreviation of the post text
    """

    if len(comment_container['post']) > 0:
        return comment_container['post'][:15]
