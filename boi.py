from flask import *
app = Flask(__name__)

@app.route('/')
def yeetiguess():
    return render_templates("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9090")
