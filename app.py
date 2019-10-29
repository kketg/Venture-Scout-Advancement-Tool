from flask import Flask
from flask import render_template

from ranks import rankload
from db import database
from todo import td
from sup import pageloader

import os


def check(p):
    if os.path.exists(p):
        return True
    else:
        return False


app = Flask(__name__, static_folder="static/")


# Create instance of boi that knows rank requirements
rm = rankload()
# Create instance of DB manager
db = database("root", "toor")
# Create rankpage-generator
todo = td()
# PAgeloader instance
pl = pageloader()

# Add this email to error pages
error_contact = "matt@mattcompton.me"


def signInAlert(type):
    if(type == "password"):
        return "Error: Incorrect Login"
    if(type == "refresh"):
        return "Error: You refreshed the page"
    else:
        return "Unknown Error"


# Get style
def style():
    return pl.gethtml("kris_style")


# Render homepage w/ default template
@app.route("/")
def yeetiguess():
    ac = pl.gethtml("main")
    return render_template("template.html", header="Home", body=ac, style=style())


# Return a 404 page if user does an oopsie
@app.errorhandler(404)
def fof(e):
    return render_template(
        "template.html",
        header="Error: 404",
        body="""<p>Couldn't find what you were looking for.<br>If you
    typed the URL manually, please check it carefully.<br>Otherwise,
    please get in touch with the developer at """
        + error_contact
        + "</p>",
        style=style(),
    )


# Return a 500 page if me or Krii does an oopsie
@app.errorhandler(500)
def err(e):
    return render_template(
        "template.html",
        header="Error: 500",
        body="""
    <p>Something's gone wrong in the code. As this app is in beta,
    chances are, you did nothing wrong. Please try again, but
    if you keep getting this message, please email:"""
        + error_contact
        + "</p>",
        style=style(),
    )


# User auth form
@app.route("/signin/user/")
def usr_sign():
    return render_template("signin.html", type="user", style=style())


# Method to display a page of all requirements for user
@app.route("/adv/<un>/<passw>/")
def adv(un, passw):
    if db.checkpassw(un, passw):
        with open("u_auth", "w") as f:
            f.write(un)
        return render_template("redirect.html", destination="/myadvancement")
    else:
        # If wrong password, tell user they dumb
        return render_template(
            "signin.html", type="user", alert=signInAlert("password"), style=style()
        )
        # return render_template(
        #    "template.html",
        #    header="Password oopsie",
        #    body="<p>Wrong password for " + un + "</p>",
        #    style=style(),
        # )


# Return todo pg:
@app.route("/myadvancement")
def myad():
    if check("u_auth"):
        with open("u_auth") as f:
            un = f.read()
        os.remove("u_auth")
        done, todos = todo.do(un)
        # Return finished page to user
        return render_template(
            "template.html",
            header="Stats for " + db.getRealName(un),
            body="<h3>Complete: </h3><hr>"
            + done
            + "<br><h3>Incomplete:</h3><hr>"
            + todos,
            style=style(),
        )
    else:
        return render_template(
            "signin.html", type="user", alert=signInAlert("refresh"), style=style()
        )


# Return a page generated from all the available ranks
@app.route("/ranks")
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
    return render_template(
        "template.html",
        header="All venture ranks",
        body=bodi,
        footer="<p>Data - 2019</p>",
        style=style(),
    )


## END NON-ADMIN FUNCTIONS ##


# Admin login form
@app.route("/signin/admin/")
def ad_sign():
    return render_template("signin.html", type="admin", style=style())


# Admin page auth (to hide admin login from URL bar)
@app.route("/auth/admin/<username>/<password>/")
def ad_redirect(username, password):
    if db.authadmin(username, password):
        with open("a_auth", "w") as f:
            f.write("ok")
        return render_template(
            "redirect.html",
            label="Admin Portal",
            destination="/management",
            style=style(),
        )
    else:
        return render_template(
            "signin.html", type="admin", alert=signInAlert("admin"), style=style()
        )


# Actual admin page here (eventually)
@app.route("/management")
def m_portal():
    if check("a_auth"):
        os.remove("a_auth")
        return render_template(
            "template.html", body=pl.gethtml("manage"), style=style()
        )
    else:
        return render_template(
            "signin.html", type="admin", alert=signInAlert("refresh"), style=style()
        )


# Method to mark requirement of rank done for user
@app.route("/md/<un>/<rank>/<req>/")
def md(un, rank, req):
    status = db.markcomplete(un, rank, req)
    return render_template("simple.html", body="<p>" + status + "</p>")


@app.route("/scout/<un>/")
def sm_scout_display(un):
    done, todos = todo.do(un)
    # Return data to be embedded
    return render_template("simple.html", body=done + "<hr>" + todos)


@app.route("/ns/<un>/<sn>/<sp>")
def addscout(un, sn, sp):
    stat = db.addscout(un, sp, sn)
    return render_template("simple.html", body="<p>" + stat + "</p>")


if __name__ == "__main__":

    # Run black linter to ficc any bad code
    os.system("python lint.py")

    db.addscout("dummyscout", "samplepassword", "John Doe")

    app.run(host="0.0.0.0", port="9090", debug=True)
