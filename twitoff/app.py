from flask import Flask, render_template
from twitoff.models import DB, User, Tweet


def create_app():
    app = Flask(__name__)


    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    DB.init_app(app)


    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('base.html', title="Home", users=users)


    app_title = "TwitOff"


    @app.route("/test")
    def test():
        return f"<p>Another { app_title } page</p>"


    @app.route("/hola")
    def hola():
        return "Hola TwitOff!"
    

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return """The db has been reset.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/populate'>Go to Populate</a>"""
    

    @app.route("/populate")
    def populate():
        oliver = User(id=1, username='oliver')
        DB.session.add(oliver)
        ariana = User(id=2, username='ariana')
        DB.session.add(ariana)
        tweet1 = Tweet(id=1, text='this is a tweet', user=oliver)
        DB.session.add(tweet1)
        DB.session.commit()
        return """Created some users.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/populate'>Go to Populate</a>
        """


    return app
