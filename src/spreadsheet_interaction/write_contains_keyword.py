import os
import pandas as pd

writer = pd.ExcelWriter(os.path.join('output', 'contains_keyword.xlsx'))


def write_data_that_contains_keyword(post_comments, keyword):
    for post in post_comments:
        process_post(post, keyword)

    writer.save()


def process_post(post, keyword):
    if 'message' in post:
        dictionary = {'post': post['message'], 'comment': []}
        for comment in post['comments']:
            process_comment(keyword, comment, dictionary)

        write_contains_keyword_to_excel(dictionary, keyword)


def process_comment(keyword, comment, dictionary):
    if keyword in comment['message'].lower():
        dictionary['comment'].append(comment['message'])


def write_contains_keyword_to_excel(dictionary, keyword):
    dataframe = pd.DataFrame(data=dictionary)
    dataframe.to_excel(writer, keyword)