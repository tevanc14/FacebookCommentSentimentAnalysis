import os
import pandas as pd

writer = pd.ExcelWriter(os.path.join('output', 'sentiment.xlsx'))


def write_sentiment_data(sentiment_analysis):
    for post in sentiment_analysis:
        process_post(post)

    writer.save()


def process_post(post):
    if 'post' in post:
        positives = {'post': post['post'], 'text': [], 'score': []}
        negatives = {'post': post['post'], 'text': [], 'score': []}
        for comment in post['comments']:
            process_comment(comment, positives, negatives)

        write_sentiment_to_excel(positives, negatives)


def process_comment(comment, positives, negatives):
    if 'score' in comment['textSentiment']['documentSentiment']:
        if comment['textSentiment']['documentSentiment']['score'] > 0:
            add_comment(comment, positives)
        else:
            add_comment(comment, negatives)


def add_comment(comment, dictionary):
    dictionary['text'].append(comment['text'])
    dictionary['score'].append(
        comment['textSentiment']['documentSentiment']['score'])


def write_sentiment_to_excel(positives, negatives):
    dataframe_positive = pd.DataFrame(data=positives)
    dataframe_negative = pd.DataFrame(data=negatives)

    dataframe_positive.to_excel(
        writer, 'Positive - ' + get_post_abbreviation(positives))
    dataframe_negative.to_excel(
        writer, 'Negative - ' + get_post_abbreviation(negatives))


def get_post_abbreviation(dictionary):
    if len(dictionary['post']) > 0:
        return dictionary['post'][:15]
