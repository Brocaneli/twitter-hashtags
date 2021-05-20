import flask
import mysql.connector as connector
import os

from flask import request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = flask.Flask(__name__)
metrics = PrometheusMetrics(app)
app.config["DEBUG"] = False

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD")

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Hello</h1>
<p>API to read data stored from Twitter</p>'''

@app.errorhandler(404)
@metrics.counter('error', 'Number of invocations by type')
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/tweets/all', methods=['GET'])
def tweets_all():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_tweets = "SELECT * FROM Tweets"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_tweets)
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/api/v1/resources/tweets', methods=['GET'])
def tweets_filter():
    query_params = request.args

    language = query_params.get('lang')
    hashtag = query_params.get('hash')
    author = query_params.get('author_id')

    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_tweets_filtered = "SELECT * FROM Tweets WHERE"

    if language:
        get_tweets_filtered += " language='{}' AND".format(language)
    if hashtag:
        get_tweets_filtered += " Hashtags_name='{}' AND".format(hashtag)
    if author:
        get_tweets_filtered += " Users_idUsers='{}' AND".format(author)
    if not (language or hashtag or author):
        return page_not_found(404)

    get_tweets_filtered = get_tweets_filtered[:-4]

    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_tweets_filtered)
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/api/v1/resources/tweets/by_hour', methods=['GET'])
def tweets_by_hour():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_tweets = "SELECT count( idTweets ) , date_format( date, '%Y-%m-%d %H' ) as my_date from Tweets GROUP BY my_date order by 'date'"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_tweets)
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/api/v1/resources/tweets/by_lang', methods=['GET'])
def tweets_by_lang():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_tweets = "select Hashtags_name, language, count(idTweets) from Tweets group by Hashtags_name, language"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_tweets)
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/api/v1/resources/users/all', methods=['GET'])
def users_all():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_users = "SELECT * FROM Users"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_users)
    result = cursor.fetchall()

    return jsonify(result)

@app.route('/api/v1/resources/users/top5', methods=['GET'])
def users_top5():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_users = "SELECT * FROM Users ORDER BY followers DESC;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_users)
    result = cursor.fetchall()[0:5]

    return jsonify(result)
    

@app.route('/api/v1/resources/hashtags/all', methods=['GET'])
def hashtags_all():
    conn = connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host='db', database='twitter')
    get_hashtags = "SELECT * FROM Hashtags"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(get_hashtags)
    result = cursor.fetchall()

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)