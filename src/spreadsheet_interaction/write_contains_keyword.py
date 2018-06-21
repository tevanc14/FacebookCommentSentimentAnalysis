import os
import pandas as pd


class ContainsKeywordWriter():
    def __init__(self, keyword):
        self.keyword = keyword
        self.comment_container = {'post': '', 'comment': []}
        self.writer = pd.ExcelWriter(
            os.path.join('output', 'contains_keyword.xlsx'))

    def write_data_that_contains_keyword(self, post_comments):
        """Write comments that contain a keyword to a spreadsheet.
        
        Arguments:
            post_comments {list} -- Posts with their respective comments
        """

        for post in post_comments:
            self.process_post(post)

        self.writer.save()

    def process_post(self, post):
        """Iterate through posts to process their comments.
        
        Arguments:
            post {dict} -- Post with its respective comments
        """

        if 'message' in post:
            self.comment_container['post'] = post['message']
            for comment in post['comments']:
                self.process_comment(comment)

            self.write_contains_keyword_to_excel()

    def write_contains_keyword_to_excel(self):
        """Take a dictionary of comments to write to a spreadsheet."""

        dataframe = pd.DataFrame(data=self.comment_container)
        dataframe.to_excel(self.writer, self.keyword)

    def process_comment(self, comment):
        """Check if comment contains the keyword.
        
        Arguments:
            comment {dict} -- Comment on a post
        """

        if self.keyword in comment['message'].lower():
            self.comment_container['comment'].append(comment['message'])
