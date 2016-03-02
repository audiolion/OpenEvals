class Course():
    def __init__(self, coursecode, coursenum):
        self.professors = set()
        self.coursecode = coursecode
        self.coursenum = coursenum
    def addProfessor(self, professor):
        self.professors.add(professor)