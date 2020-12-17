from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

keys = open('keys.txt', 'r').read().splitlines()

api_key = keys[0]
api_key_secret = keys[1]
access_token = keys[2]
access_token_secret = keys[3]

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler, wait_on_rate_limit=True)

search_term = 'covid'
amount = 100000

tweets = tweepy.Cursor(api.search, q=search_term, lang='en').items(amount)

polarity = 0
polarityList = []

with open('data.txt', 'w', newline='') as file:
    writer = csv.writer(file)
    for tweet in tweets:
        clean_text = tweet.text.replace('RT', '')
        if clean_text.startswith(' @'):
            position = clean_text.index(':')
            clean_text = clean_text[position+2:]
        if clean_text.startswith('@'):
            position = clean_text.index(' ')
            clean_text = clean_text[position+2:]
        analysis = TextBlob(clean_text)
        time = str(tweet.created_at)
        time_clean = time.partition(' ')[2]
        writer.writerow([time_clean, analysis.polarity])

        polarity += analysis.polarity
        polarityList.append(analysis.polarity)

        print(time_clean + " - " + clean_text)

print(polarity)

polarityList.sort()

plt.hist([polarityList])
plt.xlabel("Polarity")
plt.ylabel("Frequency")
plt.title("Polarity of Tweets containing 'covid'")
plt.show()
