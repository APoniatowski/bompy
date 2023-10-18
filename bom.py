from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import subprocess
import pyttsx3
from requests.exceptions import RequestException
from contextlib import closing
import feedparser


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
                                            ['pactl', 'set-sink-volume', '0', '10%'])
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


def check_nitter_rss(usernames):
    for username in usernames:
        url = f'https://nitter.net/{username}/rss'
        feed = feedparser.parse(url)
        for entry in feed.entries:
            tweet_text = entry.title
            check_text(tweet_text)


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    if resp.status_code != 200:
        log_error(f'Bad response: {resp.status_code}')
        return False
    if content_type is None or content_type.find('html') == -1:
        log_error('Invalid Content-Type')
        return False
    return True

def log_error(e):
    print(e)


# Define the countries, verbs and extras here
countries = ['Belarus', 'Russia', 'Union State',
             'Poland', 'Lithuania', 'Latvia',
             'Estonia', 'Israel', 'Iran', 'Gaza']
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
nitter_usernames = ['disclosetv', 'warmonitors', 'thewarmonitor']

for news_site in news_sites:
    check_news(news_site)
check_nitter_rss(nitter_usernames)
