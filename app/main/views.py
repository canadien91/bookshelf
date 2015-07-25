
from flask  import render_template

from .      import main

@main.route( "/" )
def Index():
    return render_template(
        "index.html", 
    )
