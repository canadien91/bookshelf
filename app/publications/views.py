from flask import render_template, url_for

from . import publications
from ..models import APublication

@publications.route("/")
def Index():
    publications_list = APublication.query.all()
    return render_template(
        "/publications/index.html",
        publications=publications_list,
    )
