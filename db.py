import os

from ranks import rankload


def check(p):
    if os.path.exists(p):
        return True
    else:
        return False


class database:
    def __init__(self, aduser, apass):
        self.rm = rankload()
        # Check OS type for required path seperator
        if os.name == "nt":
            self.s = "\\"
        else:
            self.s = "/"
        # Base path for any file operation
        self.dbp = "data" + self.s + "db" + self.s
        # If this path doesn't exist, commit folder
        if not check(self.dbp):
            os.makedirs(self.dbp)
            # Commit root user into file
            with open(self.dbp + self.s + "auser", "w") as f:
                f.write(aduser)
            # Commit root password into file
            with open(self.dbp + self.s + "apass", "w") as f:
                f.write(apass)

    def authadmin(self, auser, apass):
        # Check if root user file exist, if so, commit read
        if check(self.dbp + self.s + "auser"):
            with open(self.dbp + self.s + "auser") as f:
                cau = f.read()
            # check if root password file exii, if so, commit read
            if check(self.dbp + self.s + "apass"):
                with open(self.dbp + self.s + "apass") as f:
                    cap = f.read()
                # if either user or password is wrong, don't let them in
                if auser != cau or apass != cap:
                    return False
                # Only if both are true, allow user to pass
                else:
                    return True
            else:
                return False
        else:
            return False

    def addscout(self, username, password, disp_name):
        # Add scout name to database root for ease of reading, and b/c am lazi
        scoutpath = self.dbp + username
        if not check(scoutpath):
            # Commit account folder
            os.makedirs(scoutpath)
            # Save password
            with open(scoutpath + self.s + "passw", "w") as f:
                f.write(password)
            # Save display name
            with open(scoutpath + self.s + "dname", "w") as f:
                f.write(disp_name)
            # Add a file for each rank, and add all req's as incomplete
            for rank in self.rm.getallranks():
                str = ""
                for requirement in self.rm.getnums(rank):
                    str += "\n" + requirement
                with open(scoutpath + self.s + rank.lower() + ".txt", "w") as f:
                    f.write(str)
            return "Created " + disp_name
        # If user already exii, commit don't
        else:
            return disp_name + " already exists. Did you mean to reset password?"

    def changepassword(self, username, oldpassword, newpassword):
        scoutpath = self.dbp + username
        # If user exists, then check password with saved correct PW, then if that's coolcool save the new password
        # Can you tell I'm getting tired and bored of writing comments?
        if check(scoutpath):
            pwf = scoutpath + self.s + "passw"
            with open(pwf) as f:
                compare = f.read()
            if compare == oldpassword:
                self.setpassword(username, newpassword)
                return "Set " + username + "'s new password."
            else:
                return "Wrong current password for account. Please talk to admin"
        else:
            return "Invalid user " + username

    def setpassword(self, username, newpassword):
        # All this does is delete user's old password file, and put a new one with the new password
        scoutpath = self.dbp + username
        pwf = scoutpath + self.s + "passw"
        if check(pwf):
            os.remove(pwf)
            with open(pwf, "w") as f:
                f.write(newpassword)
            return "Changed password"
        else:
            return "Couldn't find password file"

    def markcomplete(self, username, rank, requirement):
        # Save the file for requested rank as rankfile
        scoutpath = self.dbp + username
        rankfile = scoutpath + self.s + rank + ".txt"
        # Make sure it exii
        if check(rankfile):
            with open(rankfile) as f:
                incomp = f.read()
            os.remove(rankfile)
            # Look over every line in file for the requirement to mark as done, and remove from file
            lines = incomp.split("\n")
            backtostr = ""
            for line in lines:
                if line != requirement:
                    backtostr += "\n" + line
            with open(rankfile, "w") as f:
                f.write(backtostr)
            return (
                "Marked "
                + rank
                + " requirement "
                + requirement
                + " done for "
                + username
            )
        else:
            return "Couldn't find the requested file for " + username

    def checkrankcomplete(self, username, rank):
        # Since requirements are removed when they're done, if the file is empty, it means the scout did the thing.
        scoutpath = self.dbp + username
        rankfile = scoutpath + self.s + rank + ".txt"
        if check(rankfile):
            with open(rankfile) as f:
                bois = f.read()
            # Now we have file, so check if empty
            if bois == "" or bois == "\n":
                return True
            else:
                return False

    def checkpassw(self, user, passw):
        scoutpath = self.dbp + user
        pwp = scoutpath + self.s + "passw"
        # Make sure user's password file is exii
        if check(pwp):
            with open(pwp) as f:
                correct = f.read()
            # Check if input is the same as correct password
            if correct == passw:
                return True
            else:
                return False
        else:
            return False

    def getincomplete(self, user, rank):
        scoutpath = self.dbp + user
        rankfile = scoutpath + self.s + rank + ".txt"
        # Open rank file for scout, and return all the lines in it, as that's all the to-do requirements
        if check(rankfile):
            with open(rankfile) as f:
                bois = f.read()
            return bois.split("\n")
        else:
            return "Couldn't get rank file " + rank + " for " + user

    def getRealName(self, user):
        scoutPath = self.dbp + user
        nameFile = scoutPath + self.s + "dname"
        # opens dname file
        if check(nameFile):
            name = ""
            with open(nameFile) as f:
                name = f.readline()
            # Kris this makes me sad a lil
            # but also kinda impressed.
            # can you refactor the rest of
            # this file in this way?
            name = name.split("\n")[0]
            return name
        else:
            return "Something went wrong with your account making dumbdumb"


if __name__ == "__main__":
    # Args only matter if creating DB for first time. Otherwise, these must match the ones that already are saved
    d = database("root", "toor")
    # Add scout with params
    # Requirements are remove-once-done (e.g. todo file should be empty if a scout has achieved summit)
    print(d.addscout("dummyscout", "samplepassword", "John Doe"))
    # Change password type of password reset (requires correct old password)
    # print(d.changepassword("dummyscout","samplepassword","newsamplepassword"))
    # Admin type of password reset (b/c doesn't require old password {would want to include email if we wanted self-reset but im lazy xd})
    # d.setpassword("dummyscout","dummythicc")
    # Mark requirement 10 of discovery complete for scout (acc. means delete from relevant file {but whatever})
    # d.markcomplete("dummyscout","discovery","10")
    print(d.getRealName("dummyscout"))
