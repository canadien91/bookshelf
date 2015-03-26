from ..models import APublication

def FillAPublicationForm( pk, form, pub ):
    assert type( pk ) == int

    form.title.data         = pub.title
    form.annotation.data    = pub.annotation
