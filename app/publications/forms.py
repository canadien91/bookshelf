from flask.ext.wtf      import Form
from wtforms            import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import Required, Length, Optional

class APublicationForm( Form ):
    title       = StringField( "Title", validators=[ Required(), Length( 3, 128 ) ] )
    annotation  = TextAreaField( "Annotation", validators=[ Optional() ] )
    submit      = SubmitField( "Submit" )
