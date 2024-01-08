import pickle as pkl
import tensorflow as tf
import numpy as np
from sentiment import tweet_utils

CONTEXT_PATH = "model/context.pkl"


class SentimentAnalyzer:
    def __init__(self):
        self.context = self._load_context()
        self.model = self._load_model()

        self._vocab = self.context["data.vocab"]
        self._unk_token = self.context["model.unk_token"]
        self._maxlen = self.context["model.maxlen"]


    def _load_context(self) -> dict:
        context = pkl.load(open(CONTEXT_PATH, "rb"))
        return context


    def _load_model(self) -> tf.keras.Sequential:
        context = self._load_context()
        model = tf.keras.models.load_model(context["model.sentiment_path"])
        return model

    def analyze(self, tweet: str) -> float:
        tensor = tweet_utils.tweet_to_tensor(self._vocab, tweet, self._unk_token, self._maxlen)
        return self.model.predict(tensor)[0][0]
    

    def bulk_analyze(self, tweets: list) -> list:
        tensors = []
        for tweet in tweets:
            tensors.append(tweet_utils.tweet_to_tensor(
                self._vocab, tweet, self._unk_token, self._maxlen
            ))

        return self.model.predict(np.array(tensors).reshape(-1, self._maxlen))
