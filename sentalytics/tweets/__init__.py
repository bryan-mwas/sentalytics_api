import tweepy
import sqlite3
import datetime

consumer_key = "fYYnaChhE37qSU6kny4rlDI12"
consumer_secret = "QNhX6NkQRIUuTmLFFwZNodTkGpLuST44fv8pEFUgxdZBWtv7vw"
access_token = "857505574648524803-MK21F90ay894VOK6oByNaNs6cqitmdV"
access_token_secret = "5qHwqFRayDEc7oTnV4BDNe3qooWJCBRV9GrFNyCC2pq5c"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet)
#
for tweet in tweepy.Cursor(api.search,
                           q="to:@JumiaKenya",
                           since='2016-11-25',
                           until='2016-11-27',
                           # rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():
    print(tweet.id, tweet.created_at, tweet.text, tweet.user.location)

# for tweet in tweepy.Cursor(api.search,
#                            q='to:@JumiaKenya',
#                            since='2016-11-25',
#                            until='2016-11-27',
#                            lang='en').items(10):
#     print('Tweet by: @' + tweet.user.screen_name)

def print_items():
    for tweet in tweepy.Cursor(api.search,
                               q="to:@JumiaKenya",
                               since='2016-11-25',
                               until='2016-11-27',
                               # rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
        print(tweet.id, tweet.created_at, tweet.text, tweet.user.location)


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
