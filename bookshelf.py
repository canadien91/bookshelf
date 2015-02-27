from flask import Flask
from flask import request, render_template

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
        name = form.name.data
        form.name.data = ""
    return render_template("index.html", form=form, name=name)

@app.route("/user/<name>")
def User(name):
    return render_template("user.html", name=name)

if __name__ == '__main__':
    manager.run()
