import os
import pandas as pd

from src.data_interaction import get_post_comments
from src.sentiment_analysis import get_sentiment_analysis


def data_to_excel(sentiment_analysis):
    counter = 0
    writer = pd.ExcelWriter(os.path.join('output', 'sentiment.xlsx'))
    for post in sentiment_analysis:
        if 'post' in post:
            positives = {'post': post['post'], 'text': [], 'score': []}
            negatives = {'post': post['post'], 'text': [], 'score': []}
            for comment in post['comments']:
                if 'score' in comment['textSentiment']['documentSentiment']:
                    if comment['textSentiment']['documentSentiment']['score'] > 0:
                        positives['text'].append(comment['text'])
                        positives['score'].append(comment['textSentiment'][
                            'documentSentiment']['score'])
                    else:
                        negatives['text'].append(comment['text'])
                        negatives['score'].append(comment['textSentiment'][
                            'documentSentiment']['score'])
            dataframe_positive = pd.DataFrame(data=positives)
            dataframe_negative = pd.DataFrame(data=negatives)
            dataframe_positive.to_excel(writer, 'Positive' + str(counter))
            dataframe_negative.to_excel(writer, 'Negative' + str(counter))
            counter += 1
    writer.save()


def categories_to_excel(post_comments):
    writer = pd.ExcelWriter(os.path.join('output', 'categorization.xlsx'))
    for post in post_comments:
        if 'message' in post:
            tax = {'post': post['message'], 'comment': []}
            for comment in post['comments']:
                if 'tax' in comment['message'].lower():
                    tax['comment'].append(comment['message'])
    dataframe_tax = pd.DataFrame(data=tax)
    dataframe_tax.to_excel(writer, 'Tax')
    writer.save()


if __name__ == '__main__':
    post_comments = get_post_comments(False)
    sentiment_analysis = get_sentiment_analysis(False, post_comments)
    data_to_excel(sentiment_analysis)
    categories_to_excel(post_comments)
