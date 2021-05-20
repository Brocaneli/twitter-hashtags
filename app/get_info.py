import json
import mysql.connector as connector
import requests
import os

from datetime import datetime
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

HASHTAGS = [
    "%23openbanking", 
    "%23remediation", 
    "%23devops", 
    "%23sre", 
    "%23microservices", 
    "%23observability", 
    "%23oauth", 
    "%23metrics",
    "%23logmonitoring",
    "%23opentracing"
]

TWITTER_API_URL = "https://api.twitter.com/2/tweets/search/recent?query="

TOKEN = os.getenv("TOKEN")
HEADERS = {"Authorization": "Bearer {}".format(TOKEN)}

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD")

def insert_hashtag(cursor, hashtag):
    cursor.execute("INSERT INTO Hashtags (name) VALUES ('{}')".format(hashtag.replace("%23","#")))

def insert_tweets(tweet, cursor, hashtag):
    print(tweet)
    print(cursor)
    data_tweet = (int(tweet['id']), tweet['lang'], tweet['text'], datetime.strptime(str(tweet['created_at']), "%Y-%m-%dT%H:%M:%S.%fZ"), hashtag.replace("%23","#"), int(tweet['author_id']))
    add_tweet = (
        "INSERT INTO Tweets "
        "(idTweets, language, text, date, Hashtags_name, Users_idUsers) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(add_tweet, data_tweet)

def insert_users(user, cursor):
    print(user)
    print(cursor)
    data_user = (int(user['id']), user['username'], int(user['public_metrics']['followers_count']))
    add_user = (
        "INSERT INTO Users "
        "(idUsers, username, followers) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(add_user, data_user)

def get_from_twitter(hashtag):
    query = (
        "{}"
        "&max_results=100"
        "&expansions=author_id"
        "&user.fields=public_metrics"
        "&tweet.fields=created_at,lang"
    ).format(hashtag)

    twitter_data = json.loads(requests.request("GET", "{}{}".format(TWITTER_API_URL, query), headers=HEADERS).text)

    tweets = twitter_data['data']
    users = twitter_data['includes']['users']

    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    cursor = conn.cursor()

    insert_hashtag(cursor, hashtag)

    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.map(partial(insert_users, cursor=cursor), users)

    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.map(partial(insert_tweets, cursor=cursor, hashtag=hashtag), tweets)

    conn.commit()
    conn.close()

def main():
    for hashtag in HASHTAGS:
        get_from_twitter(hashtag)

if __name__ == '__main__':
    main()