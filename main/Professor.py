#This is to group information about professors
from collections import Counter
class Professor():
    def __init__(self, firstname, lastname):
        self.commonCourse = ""
        self.courses = set()
        self.fname = firstname.capitalize()
        self.lname = lastname.capitalize()
        self.tileCourses = [] #courses that are displayed in tile
        self.ellipses = ""
    def addCourse(self, course):
        self.courses.add(course)
        if(len(self.tileCourses) < 3): #only 3 courses per tile
            self.tileCourses.append(course)

        if(len(self.tileCourses) == 3): #add the ellipses if this tile has 3 courses
            self.ellipses =  "..."
    def setCommonCourse(self):
        subjects = list()
        for course in self.courses:
            subjects.append(course.subj)
        counts = Counter(subjects)
        #(1) is to start returned list at 1st most common
        #[0] is the first [value, index] pair
        #[0] is the most common value -> what we want
        self.commonCourse = counts.most_common(1)[0][0]
