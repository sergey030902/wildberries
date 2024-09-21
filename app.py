from flask import Flask
from config import ip

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Polytech!"


if __name__ == "__main__":
    app.run(host=ip)
    app.run(debug=True)
