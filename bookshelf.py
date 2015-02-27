from flask import Flask
from flask import request, render_template, session, redirect, url_for
from flask import flash

from flask.ext.script import Manager
from flask.ext.wtf import Form

from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField("What is your name?", validators=[Required()])
    submit = SubmitField("Submit")

app = Flask(__name__)
app.config["SECRET_KEY"] = "DumbAndDumbleDore"
app.config["WTF_CSRF_ENABLED"] = True
manager = Manager(app)

@app.route("/", methods=["GET", "POST"])
def Index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("Index"))
    return render_template("index.html", form=form, name=session.get("name"))

@app.route("/user/<name>")
def User(name):
    return render_template("user.html", name=name)

if __name__ == '__main__':
    manager.run()
