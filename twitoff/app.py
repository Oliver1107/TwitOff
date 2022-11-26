"""Configures flask app and sets route for app."""

from flask import Flask, render_template, request
from tweepy.errors import Forbidden
from twitoff.models import DB, User
from twitoff.twitter import (update_all_users, add_or_update_user,)
from twitoff.predict import predict_user
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
        try:
            users = User.query.all()
        except:
            DB.drop_all()
            DB.create_all()
            users = User.query.all()
        return render_template('base.html', users=users)

    @app.route("/user", methods=['POST'])
    @app.route("/user/<name>", methods=['GET'])
    def add_user(name=None, message=''):
        """
        Adds user to the database directly from input
        on the app.
        """
        try:
            username = name or request.values['user_name']
            try:
                if request.method == 'POST':
                    add_or_update_user(username)
                    message = f"User '{username}' succesfully added."

                tweets = User.query.filter(
                    User.username == username).one().tweets

            except Exception:
                message = f"Could not add user '{username}'."

            return render_template(
                'user.html', title=username, message=message, tweets=tweets
            )

        except UnboundLocalError:
            return render_template(
                'user.html', title='Error:', message='No username given'
            )

    @app.route('/compare', methods=['POST'])
    def compare():
        user0 = request.values['user0']
        user1 = request.values['user1']

        if user0 == user1:
            message = 'Cannot compare users to themselves.'

        else:
            try:
                prediction = predict_user(
                    user0, user1, request.values['tweet_text']
                )

                if prediction:
                    predicted_user = user1
                    other_user = user0

                else:
                    predicted_user = user0
                    other_user = user1

                message = f"""
                This tweet is more likely to be posted by '{predicted_user}'
                than '{other_user}'.
                """
            except ValueError:
                message = 'Error: No tweet was given.'

        return render_template(
            'prediction.html', title='Prediction', message=message
        )

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
        """

    @app.route("/update")
    def update():
        """
        Updates all users in database to include newest tweets.
        """
        try:
            usernames = update_all_users()
            for username in usernames:
                add_or_update_user(username)

        except Forbidden:
            return """
            Something went wrong,
            one of the accounts may be suspended.
            <a href='/'>Go Home</a>
            <a href='/reset'>Go to reset</a>
            """

        else:
            return """
            All users updated.
            <a href='/'>Go to Home</a>
            """

    return app
