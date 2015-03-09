from flask      import render_template, redirect, url_for

from .          import authors
# from ..         import db
from ..models   import AnAuthor

@authors.route( "/" )
def Index():
    list_of_authors = AnAuthor.query.order_by( AnAuthor.last_name )
    list_of_authors = list_of_authors.all()
    return render_template(
        "authors/authors.html",
        a_list=list_of_authors,
    )

@authors.route( "/<pk>/" )
def Details( pk ):
    author = AnAuthor.query.get_or_404( pk )
    return render_template(
        "authors/details.html",
        author=author,
    )
