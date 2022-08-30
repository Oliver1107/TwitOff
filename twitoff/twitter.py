"""Create or update users for the app, and transform tweets."""

import os
import tweepy
import spacy
from twitoff.models import DB, User, Tweet


key = os.getenv('TWITTER_API_KEY')
secret = os.getenv('TWITTER_API_KEY_SECRET')

twitter_auth = tweepy.OAuthHandler(key, secret)
twitter_api = tweepy.API(twitter_auth)

nlp = spacy.load('my_model/')


def vectorize_tweet(tweet_text):
    """
    Transform text from tweets into word vectors
    in order for them to work with a machine learning model.
    """
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Adds users to flask database along with their 200 most recent
    tweets. If user is already in the database, updates their tweets
    in the database to include any tweets posted since last update.
    """
    try:
        twitter_user = twitter_api.get_user(screen_name=username)
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id,
            username=username,
            newest_tweet_id=None
        )
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode='extended',
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text,
                vector=vectorize_tweet(tweet.full_text),
                user_id=db_user.id,
                user=db_user
            )
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        DB.session.commit()


def update_all_users():
    """
    Gives a list of all users in database in order to
    update any user with tweets not in the database.
    """
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)
    return usernames
