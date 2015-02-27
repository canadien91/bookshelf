# This is shit-code, kids
# Don't try it at home!

import os

from flask import Flask
from flask import request, render_template, session, redirect, url_for
from flask import flash

from flask.ext.script import Manager
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand

from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField("What is your name?", validators=[Required()])
    submit = SubmitField("Submit")

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "DumbAndDumbleDore"
app.config["WTF_CSRF_ENABLED"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)

class ARole(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("AnUser", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<ARole %r>" % self.name

class AnUser(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<AnUser %r>" % self.username

@app.route("/", methods=["GET", "POST"])
def Index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = AnUser.query.filter_by(username=form.name.data).first()
        if user is None:
            user = AnUser(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            # flash("Unknown user")
        else:
            session["known"] = True
            # flash("Known user")
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("Index"))
    return render_template(
        "index.html", 
        form=form, 
        name=session.get("name"), 
        known=session.get("known", False)
    )

def make_shell_context():
    return dict(
        app=app,
        db=db,
        AnUser=AnUser,
        ARole=ARole
    )

manager.add_command( "shell", Shell( make_context=make_shell_context ) )
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
