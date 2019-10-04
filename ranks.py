import os
def check(p):
    if os.path.exists(p):
        return True
    else:
        return False

class rankload:
    def __init__(self):
        if os.name == "nt":
            self.s = "\\"
        else:
            self.s = "/"
        self.path = "data"+self.s+"ranks"+self.s
        if not check(self.path):
            print("Data don't exii")
            quit()
    def getlines(self,file):
        if check(file):
            with open(file) as f:
                raw = f.read()
            lines = raw.split("\n")
            return lines
    def getallreqs(self,rank):
        file = self.path + self.s + rank + ".txt"
        return self.getlines(file)
    def getallranks(self):
        names = []
        for file in os.listdir(self.path):
            names.append(file.replace(".txt",""))
        return names
    def getnums(self,rank):
        file = self.path + self.s + rank + ".txt"
        lines = self.getlines(file)
        nums = []
        for line in lines:
            if line != "\n" and line != "" and line != " ":
                rn = line[0]
                if rn not in nums:
                    nums.append(rn)
                else:
                    take_two = line[0] + line[1]
                    if take_two not in nums:
                        nums.append(take_two)
        return nums


if __name__ == "__main__":
    r = rankload()
    # List all rank files we have 
    print(r.getallranks())
    # Get just the numbers of each requirement, not the text w/ them
    print(r.getnums('discovery'))
    # Get the numbers and their descriptions
    print(str(r.getallreqs('discovery')))
