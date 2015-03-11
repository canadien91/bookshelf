from flask.ext.wtf      import Form
from wtforms            import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import Required, Length, Optional

class AnAuthorForm( Form ):
    first_name  = StringField( "First Name", validators=[ Required(), Length( 3, 64 ) ] )
    second_name = StringField( "Second Name", validators=[ Length( 0, 64 ) ] )
    third_name  = StringField( "Third Name", validators=[ Length( 0, 64 ) ] )
    last_name   = StringField( "Last Name", validators=[ Required(), Length( 3, 64 ) ] )

    birth_day   = DateField( "Birth Day", validators=[ Required() ] )
    death_day   = DateField( "Death Day", validators=[ Optional() ] )

    bio         = TextAreaField( "Bio" )

    submit      = SubmitField( "Submit" )
