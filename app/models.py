
from datetime           import datetime

from flask.ext.login    import UserMixin

from werkzeug.security  import generate_password_hash
from werkzeug.security  import check_password_hash

from .                  import db
from .                  import login_manager

authorship = db.Table(
    "authorship",
    db.Column( "author_id", db.Integer, db.ForeignKey( "authors.id" ) ),
    db.Column( "publication_id", db.Integer, db.ForeignKey( "publications.id" ) )
)

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

    def __repr__( self ):
        return "<AnUser %r>" % self.username

class AnAuthor( db.Model ):
    __tablename__   = "authors"
    id              = db.Column( db.Integer, primary_key=True )
    added           = db.Column( db.DateTime, default=datetime.utcnow() )

    first_name      = db.Column( db.String( 64 ) )
    second_name     = db.Column( db.String( 64 ), nullable=True )
    third_name      = db.Column( db.String( 64 ), nullable=True )
    last_name       = db.Column( db.String( 64 ), index=True, default="Tolkien" )

    birth_day       = db.Column( db.DateTime )
    death_day       = db.Column( db.DateTime, nullable=True )

    bio             = db.Column( db.Text, nullable=True )

    publications    = db.relationship(
        "APublication",
        secondary=authorship,
        backref=db.backref( "authors", lazy="dynamic" ),
        passive_deletes=True,
    )

    def __repr__( self ):
        return "<Author %s. %s>" % ( self.first_name[ 0 ], self.last_name )

    def AddPublication( self, pk=0 ):
        assert type(pk) == int
        pub = APublication.query.get_or_404(pk)
        assert pub not in self.publications
        self.publications.append( pub )
        
        db.session.add( self )
        db.session.add( pub )
        db.session.commit()

    def RemovePublication( self, pk=0 ):
        assert type( pk ) == int
        pub = APublication.query.get_or_404(pk)
        assert pub in self.publications

        self.publications.remove( pub )
        
        db.session.add( self )
        db.session.add( pub )
        db.session.commit()

class APublication( db.Model ):
    __tablename__   = "publications"

    id              = db.Column( db.Integer, primary_key=True )
    added           = db.Column( db.DateTime, default=datetime.utcnow() )

    title           = db.Column( db.String( 128 ), index=True, default="No Title" )
    annotation      = db.Column( db.Text, nullable=True )

    def __repr__( self ):
        return "<Publication #%i. %r>" % ( self.id, self.title )

@login_manager.user_loader
def LoadUser( user_id ):
    return AnUser.query.get( int( user_id ) )
