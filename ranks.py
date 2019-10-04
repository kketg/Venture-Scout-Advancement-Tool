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
    print(r.getnums('discovery'))
