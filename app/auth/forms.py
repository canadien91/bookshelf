
from flask.ext.wtf      import Form

from wtforms            import StringField, PasswordField, BooleanField, SubmitField
from wtforms            import ValidationError
from wtforms.validators import Required, Length, Regexp, EqualTo

from ..models           import AnUser

class LoginForm( Form ):
    username    = StringField( "Username", validators=[ Required() ] )
    password    = PasswordField( "Password", validators=[ Required() ] )
    remember_me = BooleanField( "Keep me logged in" )
    submit      = SubmitField( "Log In" )

class RegistrationForm( Form ):
    username        = StringField(
        "Username", 
        validators=[
            Required(),
            Length( 3, 64 ),
            Regexp( "^[A-Za-z][A-Za-z0-9_.]*$", 0, "Usernames must have only letters, numbers, dots or underscores." )
        ]
    )
    password        = PasswordField(
        "Password",
        validators=[
            Required(),
            EqualTo( "confirm_passwd", message="Passwords must match." )
        ]
    )
    confirm_passwd  = PasswordField( "Confirm Password", validators=[ Required() ] )
    submit          = SubmitField( "Register" )

    def validate_username( self, field ):
        if AnUser.query.filter_by( username=field.data ).first():
            raise ValidationError( "Username already in use." )
