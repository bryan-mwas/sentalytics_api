import tweepy
import sqlite3

consumer_key = "fYYnaChhE37qSU6kny4rlDI12"
consumer_secret = "QNhX6NkQRIUuTmLFFwZNodTkGpLuST44fv8pEFUgxdZBWtv7vw"
access_token = "857505574648524803-MK21F90ay894VOK6oByNaNs6cqitmdV"
access_token_secret = "5qHwqFRayDEc7oTnV4BDNe3qooWJCBRV9GrFNyCC2pq5c"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

jumia_tweets = api.search("q=to:@JumiaKenya")
for tweet in jumia_tweets:
    print(tweet.user.location)


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
            c.execute("INSERT INTO sentalytics_tweet (tweet_id,username,text,location,date) VALUES (?,?,?,?,?)",
                      (tweet.id, tweet.user.name, tweet.text, tweet.user.location,
                       tweet.created_at))

        # Save (commit) the changes
        conn.commit()

    except Exception as err:
        print('Query Failed: %s\nError: %s' % ("INSERT INTO sentalytics_tweet", str(err)))

    finally:
        conn.close()
