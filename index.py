import os
import pandas as pd

from src.data_interaction import get_post_comments
from src.sentiment_analysis import get_sentiment_analysis
from src.spreadsheet_interaction.write_sentiment_data import write_sentiment_data
from src.spreadsheet_interaction.write_contains_keyword import write_data_that_contains_keyword


def get_spreadsheet_of_sentiment():
    post_comments = get_post_comments(False)
    sentiment_analysis = get_sentiment_analysis(False, post_comments)
    write_sentiment_data(sentiment_analysis)
    write_data_that_contains_keyword(post_comments, 'tax')


def categories_to_excel(post_comments):
    writer = pd.ExcelWriter(os.path.join('output', 'categorization.xlsx'))
    tax = {'post': [], 'comment': []}
    for post in post_comments:
        if 'message' in post:
            for comment in post['comments']:
                if 'tax' in comment['message'].lower():
                    tax['post'].append(post['message'])
                    tax['comment'].append(comment['message'])
    dataframe_tax = pd.DataFrame(data=tax)
    dataframe_tax.to_excel(writer, 'Tax')
    writer.save()


if __name__ == '__main__':
    get_spreadsheet_of_sentiment()

# TODO: Move to classes?
# TODO: Combine common functions into util file (get abbreviation, read json file)
# TODO: README
# TODO: Rename anything called dictionary