from flask              import render_template, url_for, redirect

from flask.ext.login    import login_required

from .                  import publications
from ..                 import db
from .forms             import APublicationForm
from ..models           import APublication

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

@publications.route( "/new/", methods=["GET", "POST"])
@login_required
def AddNew():
    form = APublicationForm()
    if form.validate_on_submit():
        new_publication             = APublication()
        new_publication.title       = form.title.data
        new_publication.annotation  = form.annotation.data

        db.session.add( new_publication )
        db.session.commit()

        return redirect(url_for("publications.Details", pk=new_publication.id))
    return render_template(
        "publications/new.html",
        form=form,
    )
