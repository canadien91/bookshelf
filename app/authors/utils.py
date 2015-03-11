from ..models import AnAuthor

def FillAnAuthorForm( pk, form ):
    assert type( pk ) == int
    author = AnAuthor.query.get( pk )
    if author is not None:
        form.first_name.data    = author.first_name
        form.second_name.data   = author.second_name
        form.third_name.data    = author.third_name
        form.last_name.data     = author.last_name

        form.birth_day.data     = author.birth_day

        if author.death_day is not None:
            form.death_day.data = author.death_day

        form.bio.data = author.bio
