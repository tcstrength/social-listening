# social-listening
Do sentiment analysis to score a `keyword` on the social networking sites. My aim is to score the business, however, it is far from that destination!

## Docker compose
```bash
docker compose up
```

Access the virtual machine: http://localhost:4444. Then choose the session that holds the selenium session.

## Sentiment analysis
The dataset is used to build the model is: https://www.kaggle.com/datasets/linhlpv/vietnamese-sentiment-analyst/data, thanks to `L3VIEVIL`. The accuracy of the model is `0.875` on test dataset which is randomly chosen `10%` from the original dataset.

Here is the summary of model:

```python
Model: "sequential_8"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_6 (Embedding)     (None, 128, 128)          201600    
                                                                 
 lstm_6 (LSTM)               (None, 100)               91600     
                                                                 
 dense_6 (Dense)             (None, 1)                 101       
                                                                 
=================================================================
Total params: 293301 (1.12 MB)
Trainable params: 293301 (1.12 MB)
Non-trainable params: 0 (0.00 Byte)
```

## Comment crawler
Thanks to `longnd-1038` for his [crawler_facebook_comment](https://github.com/longnd-1038/crawler_facebook_comment), from that I can go further.

## Current status
The current score depends a lot in how the Facebook search engine works. For each keyword, I look for all posts from the Facebook search results and then the comments of the posts. The model predicts the sentiment score for comments and take average as representation. 

There are a lot of comments that mixed between Eng/Vie but the current model is only able to predict score for the Vie. 

## Further work
The sentiment analysis model must be able to score only both Eng and Vie, and has the ability to address the named entity in a sentence to make sure that the comments are exactly related to the keyword.

Besides, need to identify the languages before performing sentiment analysis.
