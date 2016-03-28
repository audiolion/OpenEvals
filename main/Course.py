#This is to group information about courses
from collections import Counter
class Course():
    def __init__(self, desc, subj, classcatnbr, title):
        self.title = title
        self.subj = subj.upper()
        self.classcatnbr = classcatnbr
        self.professors = set()
        self.ellipses = ""
        self.numSections = 0
        self.campus = set()
    def getName(self):
        return self.code + "-" + self.number

    def addProfessor(self, prof):
        if len(self.professors) < 3:
            self.professors.add(prof)
        if(len(self.professors) == 3):
            self.ellipses = "..."

    def addCampus(self, c):
        if c == 'MAI':
            self.campus.add("Rochester")
        elif c == 'CDB':
            self.campus.add("Dubrovnik")
        elif c == 'CZA':
            self.campus.add("Zagreb")
        elif c == 'DUB':
            self.campus.add("Dubai")
        else:
            self.campus.add(c)
