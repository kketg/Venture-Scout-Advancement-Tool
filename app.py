from flask import *
from ranks import rankload

app = Flask(__name__)
rm = rankload()

error_contact = "matt@mattcompton.me"

@app.route('/')
def yeetiguess():
    return render_template("template.html",header="Home")

@app.errorhandler(404)
def fof(e):
    return render_template("template.html",header="Error: 404",
    body="""<p>Couldn't find what you were looking for.<br>If you
    typed the URL manually, please check it carefully.<br>Otherwise,
    please get in touch with the developer at """ + error_contact + "</p>")

@app.errorhandler(500)
def err(e):
    return render_template("template.html",header="Error: 500",
    body="""
    <p>Something's gone wrong in the code. As this app is in beta,
    chances are, you did nothing wrong. Please try again, but
    if you keep getting this message, please email:""" + error_contact + "</p>")



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
