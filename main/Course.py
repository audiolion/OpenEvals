#This is to group information about courses
from collections import Counter
class Course():
    def __init__(self, desc, subj, classcatnbr):
        self.title = ""
        for descword in desc.split():
            self.title += descword.capitalize() + ' '
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
