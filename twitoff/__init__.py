"""Steps to perform once app is ran."""

from twitoff.app import create_app
from twitoff.models import DB


APP = create_app()
