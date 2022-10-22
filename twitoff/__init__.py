"""Steps to perform once app is ran."""

from twitoff.app import create_app
from twitoff.models import DB


DB.drop_all()
DB.create_all()

APP = create_app()
