import re
import numpy as np
import pandas as pd
import tensorflow as tf
from collections import Counter
from nltk.tokenize import TweetTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = TweetTokenizer()

def process_tweet(s: str) -> str:
    s = re.sub(r'\$\w*', '', s)
    s = re.sub(r'^RT[\s]+', '', s)
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s)
    s = re.sub(r'#', '', s)
    s = s.lower()
    s = tokenizer.tokenize(s)
    return s


def build_vocab(
    counter: Counter, min_freq: int, tweets: list, unk_token: str="__<UNK>__"
) -> dict:
    vocab = {
        unk_token: 1, "__<PAD>__": 2
    }

    for tweet in tweets:
        tweet = process_tweet(tweet)
        for word in tweet:
            if word not in vocab and counter[word] >= min_freq:
                vocab[word] = len(vocab)

    return vocab


def build_counter(tweets: list) -> dict:
    result = []
    for tweet in tweets:
        tweet = process_tweet(tweet)
        result += tweet
    return Counter(result)


def tweet_to_tensor(
    vocab: dict, tweet: str, unk_token: str = "__<UNK>>__", 
    maxlen: int=128, verbose: str = False
) -> np.ndarray:
    
    tweet = process_tweet(tweet)
    tensor = []
    unk_id = vocab[unk_token]

    if verbose:
        print(f"The unique integer ID for the unk_token is: {unk_id}")
        
    for word in tweet:
        word_id = vocab.get(word, unk_id)
        tensor.append(word_id)
    
    tensor = np.array(tensor)
    tensor = pad_sequences([tensor], padding="pre", maxlen=maxlen, truncating="pre")
    return tensor