import six
import sys

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.protobuf.json_format import MessageToDict, MessageToJson
from langdetect import detect


class SentimentAnalysis():
    def __init__(self):
        self.client = language.LanguageServiceClient()

    def sentiment_text(self, text):
        """Detects sentiment in the text.

        :param text: The text to be analyzed
        :returns: Sentiment data for given text

        """

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Instantiates a plain text document
        document = types.Document(
            content=text, type=enums.Document.Type.PLAIN_TEXT)

        return MessageToDict(self.client.analyze_sentiment(document))

    def entity_sentiment_text(self, text):
        """Detects entity sentiment in the provided text.

        :param text: The text to be analyzed
        :returns: Entity sentiment data for given text

        """

        # Entity analysis only available in english
        try:
            if detect(text) != 'en':
                return None
        except:
            return None

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text.encode('utf-8'), type=enums.Document.Type.PLAIN_TEXT)

        # Detect and send native Python encoding to receive correct word offsets
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16

        return MessageToDict(
            self.client.analyze_entity_sentiment(document, encoding))
