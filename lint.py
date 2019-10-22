import os

for file in os.listdir():
    if ".py" in file:
        os.system("black " + file)
