from flask import *
from ranks import rankload

app = Flask(__name__)
rm = rankload()

@app.route('/')
def yeetiguess():
    return render_template("template.html",header="Home")

@app.errorhandler(404)
def fof():
    return render_template(header="Error: 404",
    body="""<p>Couldn't find what you were looking for.<br>If you
    typed the URL manually, please check it carefully. """)

@app.route('/ranks')
def allranks():
    bodi = ""
    for rank in rm.getallranks():
        lines = rm.getallreqs(rank)
        thisrank = "<ul>"
        for line in lines:
            if line != "\n" and line != " " and line != "":
                thisrank += "<li><p>" + line + "</p></li>"
        thisrank += "</ul><hr>"
        bodi += "<h3>" + rank + "</h3><br>" + thisrank
    return render_template("template.html",
    header="All venture ranks",
    body=bodi,footer="<p>Data - 2019</p>")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9090", debug=True)
