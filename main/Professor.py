#This is to group information about professors
from collections import Counter
class Professor():
    def __init__(self, firstname, lastname):
        self.commonCourse = ""
        self.courses = set()
        self.fname = firstname
        self.lname = lastname
    def addCourse(self, course):
        self.courses.add(course)
    def setCommonCourse(self):
        codes = list()
        for course in self.courses:
            codes.append(course[:4])
        counts = Counter(codes)
        self.commonCourse = counts.most_common(1)[0][0]
