from flask      import render_template, url_for

from .          import publications
from ..models   import APublication

@publications.route( "/" )
def Index():
    publications_list = APublication.query.all()
    return render_template(
        "/publications/index.html",
        publications=publications_list,
    )

@publications.route( "/<int:pk>/" )
def Details( pk ):
    publication = APublication.query.get_or_404( pk )
    return render_template(
        "/publications/details.html",
        publication=publication,
    )
