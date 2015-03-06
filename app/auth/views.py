from flask              import render_template, redirect, request, url_for, flash

from flask.ext.login    import login_user
from flask.ext.login    import logout_user, login_required

from .                  import auth
from ..                 import db
from ..models           import AnUser
from .forms             import LoginForm, RegistrationForm

@auth.route( "/login", methods=[ "GET", "POST" ] )
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AnUser.query.filter_by( username=form.username.data ).first()
        if user is not None and user.VerifyPassword( form.password.data ):
            login_user( user, form.remember_me.data )
            return redirect( request.args.get( "next" ) or url_for( "main.Index" ) )
        else:
            flash( "Invalid username or password." )
    return render_template( "auth/login.html", form=form )

@auth.route( "/logout" )
@login_required
def Logout():
    logout_user()
    flash( "Goodbye!" )
    return redirect( url_for( "main.Index" ) )

@auth.route( "/register", methods=[ "GET", "POST" ] )
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = AnUser(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add( user )
        db.session.commit()
        flash( "You can now login." )
        return redirect( url_for( "auth.Login" ) )
    return render_template( "auth/register.html", form=form )
