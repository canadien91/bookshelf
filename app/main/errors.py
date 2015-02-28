# coding: utf-8

from flask  import render_template

from .      import main

@main.app_errorhandler( 404 )
def PageNotFound( error ):
    return render_template( "404.html" ), 404

@main.app_errorhandler( 500 )
def InternalServerError( error ):
    return render_template( "500.html" ), 500
