"""Creates database with user and tweet tables."""

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    """
    Creates User table and columns.

    ...

    Columns
    -------
    id : int
        unique id for the user.
    username : str
        screen name of the user's account.
    newest_tweet_id : int
        id of the user's last tweet.
    """
    id = DB.Column(
        DB.BigInteger,
        primary_key=True
    )
    username = DB.Column(
        DB.String,
        nullable=False
    )
    newest_tweet_id = DB.Column(
        DB.BigInteger
    )

    def __repr__(self) -> str:
        return f"<User: {self.username}>"


class Tweet(DB.Model):
    """
    Creates Tweet table.

    ...

    Columns
    -------
    id : int
        unique id for the user's tweet.
    text : str
        the text of the tweet.
    vector : pickle
        vectorized text of the tweet.
    user_id : int
        id of the user who posted tweet.
    user : User class
        User class object of user who posted tweet.
    """
    id = DB.Column(
        DB.BigInteger,
        primary_key=True
    )
    text = DB.Column(
        DB.Unicode(300)
    )
    vector = DB.Column(
        DB.PickleType,
        nullable=False
    )
    user_id = DB.Column(
        DB.BigInteger,
        DB.ForeignKey('user.id'),
        nullable=False
    )
    user = DB.relationship(
        'User',
        backref=DB.backref('tweets', lazy=True)
    )

    def __repr__(self) -> str:
        return f"<Tweet: {self.text}>"
