from flask import Flask
from flask import request, render_template

from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route("/")
def Index():
    # user_agent = request.headers.get("User-Agent")
    return render_template("index.html")

@app.route("/user/<name>")
def User(name):
    return render_template("user.html", name=name)

if __name__ == '__main__':
    manager.run()
