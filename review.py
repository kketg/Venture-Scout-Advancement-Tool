import pylint.lint
import os

# a simple class with a write method
class WritableObject:
    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)

    def get(self):
        return self.content


done = ""

for file in os.listdir("."):
    args = [file]
    pylint_output = WritableObject()
    pylint = pylint.lint.Run(
        args, reporter=pylint.lint.ParseableTextReporter(pylint_output), exit=False
    )
    done += "\n"
    for line in pylint_output.get():
        done += line

print(done)
