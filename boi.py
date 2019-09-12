from flask import flask
app = Flask(__name__)

@app.route('/')
def yeetiguess():
    return 'yeet'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="79125676486786786756787854")
