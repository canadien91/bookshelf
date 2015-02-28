# coding: utf-8

from flask.ext.login    import UserMixin

from werkzeug.security  import generate_password_hash
from werkzeug.security  import check_password_hash

from .                  import db
from .                  import login_manager

class ARole( db.Model ):
    __tablename__   = "roles"

    id              = db.Column( db.Integer, primary_key=True )
    name            = db.Column( db.String( 64 ), unique=True )
    users           = db.relationship( "AnUser", backref="role", lazy="dynamic" )

    def __repr__( self ):
        return "<ARole %r>" % self.name

class AnUser( UserMixin, db.Model ):
    __tablename__   = "users"

    id              = db.Column( db.Integer, primary_key=True )
    username        = db.Column( db.String( 64 ), unique=True, index=True )
    password_hash   = db.Column( db.String( 128 ) )
    role_id         = db.Column( db.Integer, db.ForeignKey( "roles.id" ) )

    @property
    def password( self ):
        raise AttributeError( "Password is not a readable attribute" )

    @password.setter
    def password( self, password ):
        self.password_hash = generate_password_hash( password )

    def VerifyPassword( self, password ):
        return check_password_hash( self.password_hash, password )

    def __repr__(self):
        return "<AnUser %r>" % self.username

@login_manager.user_loader
def LoadUser( user_id ):
    return AnUser.query.get( int( user_id ) )
