import facebook
import json
import os
import requests


class FacebookData:
    graph_api_version = '3.0'

    def __init__(self):
        self.secrets = self.get_secrets()
        self.graph = facebook.GraphAPI(
            access_token=self.secrets['access_token'],
            version=self.graph_api_version)

    def get_secrets(self):
        """Retrieve private data that doesn't go in source control.
        
        Returns:
            [dict] -- Contents of the secrets.json file
        """

        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, 'secrets.json')
        with open(file_path, 'r') as secrets_file:
            return json.load(secrets_file)

    def get_post_comments(self, fresh_data):
        """Retrieve Facebook comments on certain posts.
        
        Arguments:
            fresh_data {bool} -- Hit Facebook Graph API or read local data
        
        Returns:
            [list] -- All comments for a set of posts
        """

        if fresh_data:
            self.get_fresh_post_comments()

        with open(os.path.join('data', 'comments.json'), 'r') as comments_file:
            return json.load(comments_file)

    def get_fresh_post_comments(self):
        """Traverse the graph to get data and write it to a json file."""

        page_id = self.get_page_id()
        posts = self.get_posts(page_id)
        comments = self.get_comments(posts)
        write_post_comments(comments)

    def get_page_id(self):
        """Retrieve the page id for a certain page name.
        
        Returns:
            [string] -- Id of the page to be searched
        """

        page = self.graph.get_object(id=self.secrets['page_name'])
        return page['id']

    def get_posts(self, page_id):
        """Retrieve the posts for a page id.
        
        Arguments:
            page_id {string} -- Id of the page to be searched
        
        Returns:
            [list] -- All posts on a page
        """

        posts = self.graph.get_connections(id=page_id, connection_name='posts')
        aggregate_posts = aggregate_paginated_data(posts)
        return aggregate_posts

    def get_comments(self, posts):
        """Retrieve comments to posts.
        
        Arguments:
            posts {dict} -- Posts to get comments from
        
        Returns:
            [list] -- Posts with comments
        """

        for post in posts:
            comments = self.graph.get_connections(
                id=post['id'], connection_name='comments')
            aggregate_comments = aggregate_paginated_data(comments)
            post['comments'] = aggregate_comments

        return posts


def aggregate_paginated_data(response_data):
    """Iterate through pages of Facebook data.

    Facebook's Graph API will return a fixed number of results before it
    starts a new page of data (to avoid returning too large a number of
    things). So the data must be requested repeatedly until there are no
    pages left.
    
    Arguments:
        response_data {dict} -- The initial response from Facebook
    
    Returns:
        [list] -- The compiled results from all pages
    """

    aggregate = []
    while True:
        try:
            aggregate.extend(response_data['data'])
            response_data = requests.get(
                response_data['paging']['next']).json()
        except KeyError:
            return aggregate


def write_post_comments(post_comments):
    """Write Facebook data to json file.
    
    Arguments:
        post_comments {list} -- All posts and their comments
    """

    with open(os.path.join('data', 'comments.json'), 'w') as comments_file:
        json.dump(post_comments, comments_file)
