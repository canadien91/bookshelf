
from flask              import render_template, redirect 
from flask              import url_for, flash

from flask.ext.login    import login_required

from .                  import authors
from .forms             import AnAuthorForm
from ..                 import db
from ..models           import AnAuthor

from .utils             import FillAnAuthorForm

@authors.route( "/" )
def Index():
    list_of_authors = AnAuthor.query.order_by( AnAuthor.last_name )
    list_of_authors = list_of_authors.all()
    return render_template(
        "authors/authors.html",
        a_list=list_of_authors,
    )

@authors.route( "/<int:pk>/" )
def Details( pk ):
    author          = AnAuthor.query.get_or_404( pk )
    publications    = list( author.publications )
    publications.sort( key=lambda x: x.added )
    return render_template(
        "authors/details.html",
        author=author,
        publications=publications,
    )

@authors.route( "/new/", methods=[ "GET", "POST" ] )
@login_required
def AddNewAuthor():
    form = AnAuthorForm()
    if form.validate_on_submit():
        new_author              = AnAuthor()

        new_author.first_name   = form.first_name.data
        new_author.second_name  = form.second_name.data
        new_author.third_name   = form.third_name.data
        new_author.last_name    = form.last_name.data

        new_author.birth_day    = form.birth_day.data
        new_author.death_day    = form.death_day.data

        new_author.bio          = form.bio.data

        db.session.add( new_author )
        db.session.commit()

        flash( "You have successfully created a new author." )
        return redirect( url_for( "authors.Details", pk=new_author.id ) )

    return render_template(
        "authors/new.html",
        form=form,
    )

@authors.route( "/<int:pk>/edit/", methods=[ "GET", "POST" ] )
@login_required
def EditAuthor( pk ):
    author  = AnAuthor.query.get_or_404( pk )
    form    = AnAuthorForm()
    if form.validate_on_submit():
        author.first_name   = form.first_name.data
        author.second_name  = form.second_name.data
        author.third_name   = form.third_name.data
        author.last_name    = form.last_name.data

        author.birth_day    = form.birth_day.data
        author.death_day    = form.death_day.data

        author.bio          = form.bio.data

        db.session.add( author )
        db.session.commit()

        flash( "You have successfully updated author." )
        return redirect( url_for( "authors.Details", pk=author.id ) )

    FillAnAuthorForm( pk, form )
    return render_template(
        "authors/edit.html",
        form=form,
    )

@authors.route( "/<int:pk>/delete/" )
@login_required
def Delete( pk ):
    author = AnAuthor.query.get_or_404( pk )
    db.session.delete( author )
    db.session.commit()
    flash( "You have successfully deleted author." )
    return redirect( url_for( "authors.Index" ) )
