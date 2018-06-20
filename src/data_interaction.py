import facebook
import json
import os
import requests


def get_secrets():
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, 'secrets.json')
    with open(file_path, 'r') as secrets_file:
        return json.load(secrets_file)


secrets = get_secrets()
graph_api_version = '3.0'

graph = facebook.GraphAPI(
    access_token=secrets['access_token'], version=graph_api_version)


def get_post_comments(fresh_data):
    if fresh_data:
        get_fresh_post_comments()

    with open(os.path.join('data', 'comments.json'), 'r') as comments_file:
        return json.load(comments_file)


def get_fresh_post_comments():
    page_id = get_page_id()
    posts = get_posts(page_id)
    comments = get_comments(posts)
    write_post_comments(comments)


def get_page_id():
    page = graph.get_object(id=secrets['page_name'])
    return page['id']


def get_posts(page_id):
    aggregate_posts = []
    posts = graph.get_connections(id=page_id, connection_name='posts')
    while True:
        try:
            aggregate_posts.extend(posts['data'])
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            break
    return aggregate_posts


def get_comments(posts):
    for post in posts:
        aggregate_comments = []
        comments = graph.get_connections(
            id=post['id'], connection_name='comments')
        while True:
            try:
                aggregate_comments.extend(comments['data'])
                comments = requests.get(comments['paging']['next']).json()
            except KeyError:
                break

        post['comments'] = aggregate_comments

    return posts


def write_post_comments(comments):
    with open(os.path.join('data', 'comments.json'), 'w') as comments_file:
        json.dump(comments, comments_file)
