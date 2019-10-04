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
    print(d.addscout("dummyscout","samplepassword","John Doe"))
    print(d.changepassword("dummyscout","samplepassword","newsamplepassword"))
    d.setpassword("dummyscout","dummythicc")
