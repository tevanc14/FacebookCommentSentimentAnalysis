# Facebook Comment Sentiment Analysis

This project retrieves all posts for a given Facebook page, performs both
[sentiment analysis](https://cloud.google.com/natural-language/docs/basics#sentiment_analysis) and
[entity sentiment analysis](https://cloud.google.com/natural-language/docs/basics#entity-sentiment-analysis),
and then gathers that data into spreadsheets for valuable viewing.

## Usage

- [Get a facebook developer token](https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=1614222468654688%3Ffields%3Dabout%2Cposts%7Bcomments%7D&version=v3.0)
- Create `src/secrets.json` with the following:

```json
{
  "access_token": "This is the facebook developer token you retrieved earlier",
  "page_name": "This is the page you plan on grabbing posts/comments from"
}
```

- Install dependencies

```shell
pip install -r requirements.txt
```

- Run it

```shell
python3 index.py
```

### Facebook Graph API

The Graph API is utitlized to traverse through the graph in the following
fashion:

- Start with the node of a given page
- Get all connected post nodes
- Get all connected comment nodes
- page -> post(s) -> comment(s)

### Google Cloud Natural Language

Google Cloud Platform's natural language processing API is used to retrieve:

- Sentiment data (from -1 to +1, how positive or negative is the given text)
- Entity sentiment data (extract entities from text and similar sentiment data)

#### Caveat

If the network speed is fast enough when hitting these APIs, it is probable
that the API quota 'DefaultRequestsPerMinutePerProject' will be exceeded.

If this happens, the requests can be manually throttled with a timer to
stay within the default GCP bounds.
