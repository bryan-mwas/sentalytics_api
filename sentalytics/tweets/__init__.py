import tweepy
import sqlite3
import datetime

consumer_key = "h1p1k1Vpq0rBwZJglASXilzPp"
consumer_secret = "nmlnSg6eafn9UCDfB51YdjvFcmdsVrJ0Xv99jVSDGaEyELHnsy"
access_token = "857505574648524803-4aoZzvHGUYN9EtoN3mgPgQnlYhgK30l"
access_token_secret = "l6CYbGnqP4J3V9wKwpbRA3UyESAG08ozb7r5Y0RYWoI1W"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet)
#
    

# for tweet in tweepy.Cursor(api.search,
#                            q='to:@JumiaKenya',
#                            since='2016-11-25',
#                            until='2016-11-27',
#                            lang='en').items(10):
#     print('Tweet by: @' + tweet.user.screen_name)

def print_items():
    for tweet in tweepy.Cursor(api.search,q="to:@JumiaKenya",since='2016-11-25',until='2016-11-27',result_type="recent",include_entities=True,lang="en").items():
        try:
            print("Woot")
            print(tweet.id, tweet.created_at, tweet.text, tweet.user.location)
        except Exception as e:
            print("Woot"*2)
            print(e)


def save_to_db():
    try:
        conn = sqlite3.connect('db.sqlite3')
        if conn:
            print("Connected!")
        c = conn.cursor()
        for tweet in tweepy.Cursor(api.search,
                                   q="to:@JumiaKenya",
                                   rpp=100,
                                   result_type="recent",
                                   include_entities=True,
                                   lang="en").items():
            # print(tweet.id, tweet.created_at, tweet.text, tweet.user.location)
            # Insert a row of data
            # Convert the datetime into date
            c.execute("INSERT INTO sentalytics_tweet (tweet_id,username,text,location,created_date) VALUES (?,?,?,?,?)",
                      (tweet.id, tweet.user.name, tweet.text, tweet.user.location,
                       tweet.created_at.date()))

        # Save (commit) the changes
        conn.commit()

    except Exception as err:
        print('Query Failed: %s\nError: %s' % ("INSERT INTO sentalytics_tweet", str(err)))

    finally:
        conn.close()
