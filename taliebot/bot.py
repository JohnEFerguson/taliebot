import os
import random
import time

import tweepy

from taliebot.tweet_generator import generate_tweet_with_retries

client = tweepy.Client(
        bearer_token=os.getenv('BEARER_TOKEN'),
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_KEY_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)


def main():
    try:
        tweet_to_write = generate_tweet_with_retries()
        print(f'hey, should I tweet this |{tweet_to_write}|?')
        ans = input()
        if ans == 'yes':
            print("ok ok i'm doing it")
            client.create_tweet(text=tweet_to_write)
        else:
            print("um ok, i'll try again")
    except Exception as err:
        print(f'Failed to write tweet, err: {err}')


if __name__ == '__main__':
    while True:
        main()
        print('thinking...')
        time.sleep(random.randrange(20, 60))


