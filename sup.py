import os

# Class that yoinks raw HTML from a page in pgs/ to slap as a render_template arguement


def check(p):
    if os.path.exists(p):
        return True
    else:
        return False


class pageloader:
    def __init__(self):
        # Check OS type for required path seperator
        if os.name == "nt":
            self.s = "\\"
        else:
            self.s = "/"
        if not check("pgs"):
            os.makedirs("pgs")

    def gethtml(self, fn):
        if check("pgs" + self.s + fn + ".html"):
            with open("pgs" + self.s + fn + ".html") as f:
                return f.read()
        else:
            return (
                "<p>Couldn't load page addition: "
                + fn
                + ".<br>Please contact programmers</p>"
            )
