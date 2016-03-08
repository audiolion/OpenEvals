#This is to group information about courses
from collections import Counter
class Course():
    def __init__(self, desc, code, number):
        self.title = desc
        self.code = code
        self.number = number
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