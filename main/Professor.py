#This is to group information about professors
class Professor():
    commonCourse = ""
    def __init__(self, firstname, lastname):
        self.courses = set()
        self.fname = firstname
        self.lname = lastname
    def addCourse(self, course):
        self.courses.add(course)
    def setCommonCourse(self, courseCode):
        self.commonCourse = courseCode