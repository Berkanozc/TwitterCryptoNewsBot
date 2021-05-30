import tweepy
import requests
import schedule
import time
import config

BASE_URL = "https://newsapi.org/v2/top-headlines"
TIME_TO_POST = "10:00"


# Fetch most recent news articles from database
def get_latest_news_articles():
    request_params = "category=business&country=us&q=crypto"
    request_url = "{}?{}&apiKey={}".format(BASE_URL, request_params, config.news_api_key)
    response = requests.get(request_url).json()

    articles = []
    if response['status'] == 'ok':

        print(len(response))
        for article in response['articles']:
            articles.append(article['url'])

    return articles


# Function to start fetching news_articles and add a tweet on twitter with fetched data
def run():
    found_articles = get_latest_news_articles()

    auth = tweepy.OAuthHandler(config.twitter_consumer_key, config.twitter_consumer_secret_key)
    auth.set_access_token(config.twitter_access_token, config.twitter_access_token_secret)

    api = tweepy.API(auth)

    for article in found_articles:
        try:
            api.update_status(article)
        except:
            print("Already posted")


# Set up time to post
schedule.every().day.at(TIME_TO_POST).do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
