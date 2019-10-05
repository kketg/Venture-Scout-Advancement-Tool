# Comment to test another thing i'm working on

from flask import *
from ranks import rankload
from db import database

app = Flask(__name__)

# Create instance of boi that knows rank requirements
rm = rankload()
# Create instance of DB manager
db = database("root","toor")

# Add this email to error pages
error_contact = "matt@mattcompton.me"

# Render homepage w/ default template
@app.route('/')
def yeetiguess():
    return render_template("template.html",header="Home")

# Return a 404 page if user does an oopsie
@app.errorhandler(404)
def fof(e):
    return render_template("template.html",header="Error: 404",
    body="""<p>Couldn't find what you were looking for.<br>If you
    typed the URL manually, please check it carefully.<br>Otherwise,
    please get in touch with the developer at """ + error_contact + "</p>")

# Return a 500 page if me or Krii does an oopsie
@app.errorhandler(500)
def err(e):
    return render_template("template.html",header="Error: 500",
    body="""
    <p>Something's gone wrong in the code. As this app is in beta,
    chances are, you did nothing wrong. Please try again, but
    if you keep getting this message, please email:""" + error_contact + "</p>")

# Method to mark requirement of rank done for user
@app.route("/md/<un>/<rank>/<req>/")
def md(un,rank,req):
    status = db.markcomplete(un,rank,req)
    return render_template("template.html",header="Output of DB Command",body="<p>" + status + "</p>")

# Method to display a page of all requirements for user
@app.route("/adv/<un>/<passw>/")
def adv(un,passw):
    if db.checkpassw(un,passw):
        complete = []
        # list of all ranks in DB
        all = rm.getallranks()
        notc = []
        for rank in all:
            # Check if user has rank complete
            if db.checkrankcomplete(un,rank):
                complete.append(rank)
            else:
                notc.append(rank)

        # for each rank that's in the incomplete list, add to list to display
        # want to replace with tables at some point
        # see: https://www.w3schools.com/html/html_tables.asp
        todos = """"""
        for rank in notc:
            this = "<h4>" + rank + " todo:</h4><br><ul>"
            # Display all incomplete reqs for rank
            this_td = db.getincomplete(un,rank)
            for td in this_td:
                if td != " " and td != "" and td != "\n":
                    this += "<li><p>" + td + "</p></li>"
            this += "</ul>"
            todos += this + "<hr>"

        # for each complete rank, add to list
        done = """"""
        if complete:
            done += "<ul>"
            for rank in complete:
                done += "<li><p>" + rank + "</p></li>"
            done += "</ul>"
        else:
            done += "<p>Sorry, no ranks complete. :(</p>"

        # Return finished page to user
        return render_template("template.html",header="Stats for " + un,
        body = "<h3>Complete: </h3><hr>" + done + "<br><h3>Incomplete:</h3><hr>" + todos)
    else:
        # If wrong password, tell user they dumb
        return render_template("template.html",header="Password oopsie",
        body="<p>Wrong password for " + un + "</p>")



# Return a page generated from all the available ranks
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
