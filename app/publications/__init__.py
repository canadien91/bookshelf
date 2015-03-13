from flask import Blueprint

publications = Blueprint( "publications", __name__ )

from . import views
