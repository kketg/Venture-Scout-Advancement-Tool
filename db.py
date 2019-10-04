import os

from ranks import rankload

def check(p):
    if os.path.exists(p):
        return True
    else:
        return False

class database:
    def __init__(self):
        self.rm = rankload()
        if os.name == "nt":
            self.s = "\\"
        else:
            self.s = "/"
        self.dbp = "data"+self.s+"db"+self.s
        if not check(self.dbp):
            os.makedirs(self.dbp)
    def addscout(self,username,password,disp_name):
        scoutpath = self.dbp + username
        if not check(scoutpath):
            os.makedirs(scoutpath)
            with open(scoutpath+self.s+"passw","w") as f:
                f.write(password)
            with open(scoutpath+self.s+"dname","w") as f:
                f.write(disp_name)
            for rank in self.rm.getallranks():
                str = ""
                for requirement in self.rm.getnums(rank):
                    str += "\n" + requirement
                with open(scoutpath+self.s+rank+".txt","w") as f:
                    f.write(str)
            return "Created " + disp_name
        else:
            return disp_name + " already exists. Did you mean to reset password?"
    def changepassword(self,username,oldpassword,newpassword):
        scoutpath = self.dbp + username
        if check(scoutpath):
            pwf = scoutpath+self.s+"passw"
            with open(pwf) as f:
                compare = f.read()
            if compare == oldpassword:
                self.setpassword(username,newpassword)
                return "Set " + username + "'s new password."
            else:
                return "Wrong current password for account. Please talk to admin"
        else:
            return "Invalid user " + username
    def setpassword(self,username,newpassword):
        scoutpath = self.dbp + username
        pwf = scoutpath+self.s+"passw"
        os.remove(pwf)
        with open(pwf,"w") as f:
            f.write(newpassword)

if __name__ == "__main__":
    d = database()
    # Add scout with params
    # Requirements are remove-once-done (e.g. todo file should be empty if a scout has achieved summit)
    print(d.addscout("dummyscout","samplepassword","John Doe"))
    # Change password type of password reset (requires correct old password)
    print(d.changepassword("dummyscout","samplepassword","newsamplepassword"))
    # Admin type of password reset (b/c doesn't require old password {would want to include email if we wanted self-reset but im lazy xd})
    d.setpassword("dummyscout","dummythicc")
