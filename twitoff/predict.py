"""Implement data prediction model."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.models import User
from twitoff.twitter import vectorize_tweet


def predict_user(username0, username1, hypo_tweet_text):
    """
    Takes two twitter users and determines which is more
    likely to say a given tweet. Return 0 for the first
    user and 1 for the second.
    """
    user0 = User.query.filter(User.username == username0).one()
    user1 = User.query.filter(User.username == username1).one()

    user0_vects = np.array([tweet.vector for tweet in user0.tweets])
    user1_vects = np.array([tweet.vector for tweet in user1.tweets])

    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]
    )

    log_reg = LogisticRegression()
    log_reg.fit(vects, labels)

    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))
