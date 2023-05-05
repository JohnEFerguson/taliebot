import os
import pandas as pd
import random
from transformers import pipeline

model = pipeline("text-generation", model="gpt2")
talie_hist_tweets = t_df = pd.read_csv(f'{os.path.dirname(__file__)}/talies_tweets.csv').text.to_list()
stuff_talie_likes = ['ohio', 'midwest', 'mahjong', 'the bachelor', 'yoga', 'drop dead gorgeous the movie',
                     'dog agility', 'the G train', 'ABBA', 'weed', 'psychology', 'The Mets', 'The Sims',
                     'The University of Michigan', 'journaling', 'skincare', 'Kate Bush', 'being a Taurus',
                     'kiwis', 'dog agility']
talies_friends = ['renzi', 'josh', 'katie', 'coco', 'jane', 'victoria', 'sarah', 'claudia', 'natalie']


def replace_anon_with_friend(tweet):
    ind = tweet.index('_')
    res = tweet.replace('_', '')
    friend = talies_friends[random.randrange(len(talies_friends))]
    if len(res) == 0:
        return friend
    res = res[:ind] + friend + res[ind:]
    return res


def generate_tweet():
    hist_tweet = talie_hist_tweets[random.randrange(len(talie_hist_tweets))]
    print(f"remember when I said |{hist_tweet}|?")
    thing_talie_likes = stuff_talie_likes[random.randrange(len(stuff_talie_likes))]
    print(f"now i've got {thing_talie_likes} on my mind")
    joke_spec_hist_tweet = f'I remebered when I said {hist_tweet}, and it made me think about ' \
                           f'{thing_talie_likes} ' \
                           f'and so here is what I thought next: '
    gen_text = model(joke_spec_hist_tweet,
                     do_sample=True, top_k=50,
                     temperature=0.9, max_length=100)[0]['generated_text']
    text_without_hist = gen_text[len(joke_spec_hist_tweet):]

    # Remove newlines.
    tweet = text_without_hist.replace('\n', '')\
        .replace('"', '')\
        .replace(',', '')\
        .replace('@', '')\
        .replace('https://', '')

    # Tokenize sentences.
    tweet_sentences = tweet.split('.')
    tweet_sentences = [t for t in tweet_sentences if len(t) > 10]

    # Take the first one, lowercase.
    tweet = tweet_sentences[0].lower().strip()
    if '__' in tweet:
        tweet = replace_anon_with_friend(tweet)
    return tweet


def generate_tweet_with_retries():
    num_retries = 100
    for try_num in range(0, num_retries):
        try:
            return generate_tweet()
        except:
            print(f'Failed, trying {num_retries - try_num} more times.')
