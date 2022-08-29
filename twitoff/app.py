"""Configures flask app and sets route for app."""

from flask import Flask, render_template
from twitoff.models import DB, User, Tweet
from twitoff.twitter import (
    update_all_users,
    add_or_update_user,
    vectorize_tweet
)
import os


def create_app():
    """
    Creates the app with all of the included routes.
    """

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def root():
        """
        Home page of the app.
        """

        users = User.query.all()
        return render_template('base.html', title="Home", users=users)

    app_title = "TwitOff"

    @app.route("/test")
    def test():
        """
        Test route.
        """

        return f"<p>Another { app_title } page</p>"

    @app.route("/hola")
    def hola():
        """
        Test route greets user.
        """

        return "Hola TwitOff!"

    @app.route("/reset")
    def reset():
        """
        Resets the database to remove all users
        and tweets.
        """

        DB.drop_all()
        DB.create_all()
        return """
        The db has been reset.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/populate'>Go to Populate</a>
        """

    @app.route("/populate")
    def populate():
        """
        Populates database with fake twitter users.
        """

        oliver = User(
            id=1,
            username='oliver'
        )
        DB.session.add(oliver)
        ariana = User(
            id=2,
            username='ariana'
        )
        DB.session.add(ariana)
        tweet1 = Tweet(
            id=1,
            text='this is a tweet',
            vector=vectorize_tweet('this is a tweet'),
            user=oliver
        )
        DB.session.add(tweet1)
        DB.session.commit()
        return """
        Created some users.
        <a href='/'>Go to Home</a>
        <a href='/populate'>Go to Populate</a>
        """

    @app.route('/update')
    def update():
        """
        Updates all users in database to include newest tweets.
        """

        usernames = update_all_users()
        for username in usernames:
            add_or_update_user(username)
        return """
        All users updated.
        <a href='/'>Go to Home</a>
        """

    @app.route('/user<id>-tweets')
    def tweets(id):
        """
        Links users listed on the homepage with a collection
        of all their tweets.
        """
        
        user = User.query.get(id)
        tweets = user.tweets
        text = '<p>---</p>'.join([f'<p>{tweet.text}</p>' for tweet in tweets])
        return f"""
        <p>{user.username}'s tweets:</p>
        <p>=====</p>
        {text}
        """

    return app
