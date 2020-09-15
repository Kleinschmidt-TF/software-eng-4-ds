import datetime

from flask import Flask, render_template

app = Flask(__name__)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
@app.route("/")
def dashboard():
    return render_template("dashboard.html", date_run=now)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
