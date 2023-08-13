from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import pyttsx3
from requests.exceptions import RequestException
from contextlib import closing
import tweepy


def check_news(url):
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                soup = BeautifulSoup(resp.content, 'html.parser')
                parse_news(soup)
            else:
                print('Error during requests to {0} : {1}'.format(
                    url, str(resp.status_code)))
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))


def parse_news(soup):
    tags = ['h1', 'h2', 'h3', 'p', 'a', 'span']
    for tag_name in tags:
        for tag in soup.find_all(tag_name):
            # Get the text of the element
            text = tag.get_text()
            if len(text.split()) <= 4:
                continue
            else:
                check_text(text.strip())


def check_text(text):
    voice_message = "news message: "
    for country in countries:
        if country.lower() in text.lower():
            voice_message = voice_message + " " + country.lower()
            # If a country name is found, check for verbs
            for verb in verbs:
                if verb.lower() in text.lower():
                    voice_message = voice_message + " " + verb.lower()
                    for other_country in countries:
                        if other_country != country and other_country.lower() in text.lower():
                            voice_message = voice_message + " " + other_country.lower()
                            # If a different country is found, check for extra words
                            for word in extra:
                                if word.lower() in text.lower():
                                    # Get the current mute status
                                    output = subprocess.check_output(
                                        'pactl list sinks | grep Mute', shell=True)
                                    # If muted, unmute and set volume to 100%
                                    if 'yes' in output.decode('utf-8'):
                                        subprocess.run(
                                            ['pactl', 'set-sink-mute', '0', '0'])
                                        subprocess.run(
                                            ['pactl', 'set-sink-volume', '0', '100%'])
                                    # If an extra word is found, display a notification and play a sound
                                    voice_message = voice_message + " " + word
                                    # initialize pyttsx3
                                    voice_alert = pyttsx3.init()
                                    subprocess.run(
                                        ['notify-send', 'News Alert', voice_message])
                                    voice_alert.say(voice_message)
                                    voice_alert.runAndWait()
                                    if 'yes' in output.decode('utf-8'):
                                        subprocess.run(
                                            ['pactl', 'set-sink-mute', '0', '1'])

                                    print(voice_message)
                                    return
                                else:
                                    subprocess.run(
                                        ['notify-send', 'News Warning', voice_message])
                                    print(voice_message)
                                    return


# Might possibly depricate, as reading tweets meaningfully, is a paid for feature
def check_twitter(accounts):
    # Load .env file for twitter API tokens
    load_dotenv()

    client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'),
                           consumer_key=os.getenv('CONSUMER_KEY'),
                           consumer_secret=os.getenv('CONSUMER_SECRET'),
                           access_token=os.getenv('ACCESS_TOKEN'),
                           access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))
    voice_message = "twitter message: "

    for account in accounts:
        tweets = client.get_users_tweets(id=account)
        for tweet in tweets.data:
            # Check if any of the country names are in the tweet
            for country in countries:
                if country.lower() in tweet.text.lower():
                    voice_message = voice_message + country.lower()
                    # If a country name is found, check for verbs
                    for verb in verbs:
                        if verb.lower() and country.lower() in tweet.text.lower():
                            for other_country in countries:
                                if other_country != country and other_country.lower() in tweet.text.lower():
                                    voice_message = voice_message + verb.lower() + other_country.lower()
                                    # If a verb is found, check for extra words
                                    for word in extra:
                                        if word.lower() in tweet.text.lower():
                                            # If an extra word is found, display a notification and play a sound
                                            os.system(
                                                '''notify-send "Twitter Alert" "{}"'''.format(tweet.text))
                                            voice_message = word + voice_message
                                            return
                                else:

                                    os.system(
                                        '''notify-send "News Warning" "{}"'''.format(tweet.text))
                                    return


# just to check if we get a 200 OK response
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


# error printer for printing errors
def log_error(e):
    print(e)


# Keywords or terms to check out for
countries = ['Belarus', 'Russia', 'Union State',
             'Poland', 'Lithuania', 'Latvia', 'Estonia', 'Israel', 'Iran']
verbs = ['attacks', 'invades', 'assaults', 'advancing towards', 'advancing to']
extra = ['Wagner', 'Breaking News', 'PMC', 'mercenaries']

# Define the news sites to monitor
news_sites = ["https://www.bbc.co.uk/news",
              "https://www.disclose.tv/news",
              "https://www.rt.com/",
              "https://www.reuters.com/",
              "https://www.forbes.com/",
              "https://www.aljazeera.com/",
              "https://www.theguardian.com/international",
              "https://news.yahoo.com"]

# Define the Twitter accounts to monitor
twitter_accounts = ['disclosetv', 'warmonitors', 'thewarmonitor']
# Add more Twitter accounts here

# Run the check_news function and check_twitter function every 60 seconds
for news_site in news_sites:
    check_news(news_site)
# check_twitter(twitter_accounts)
