from ranks import rankload
from db import database


class td:
    def __init__(self):
        self.dbm = database("root", "toor")
        self.rmm = rankload()
        return

    def do(self, un):
        # This mess creates two HTML lists of: what the account has incomplete, and what they've finished

        complete = []
        # list of all ranks in self.dbm
        all = self.rmm.getallranks()
        notc = []
        for rank in all:
            # Check if user has rank complete
            if self.dbm.checkrankcomplete(un, rank):
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
            this_td = self.dbm.getincomplete(un, rank)
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

        return (done, todos)
