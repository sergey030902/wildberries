from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello Polytech!"


if __name__ == "__main__":
    app.run(host="172.20.10.5")   
    app.run(debug=True)
