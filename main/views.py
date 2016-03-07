from django.shortcuts import render
from django.shortcuts import render_to_response
from itertools import chain
from .models import *
from .Professor import *
from .Course import *

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def search(request, searchQ):
    if request.method == 'GET' and len(request.GET) > 0:
        searchData = request.GET["search"].lower()
        data = searchData.split()

        foundProfs = professorsSearch(data, searchData)
        foundCourses = coursesSearch(data, searchData)

        return render(request, 'main/search.html', {'professors': foundProfs, "courses" : foundCourses},)
    else:
        if(searchQ != ""):
            #This is solely for running a search via the common course link
            #in a professor tile. Searching via a url not yet supported
            foundCourses = coursesSearch([searchQ], searchQ)
            return render(request, 'main/search.html', {"courses" : foundCourses})
        else:
            return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    prof = EvalResults.objects.filter(instr_last_name=lastname,
                                      instr_first_name=firstname)
    questions = EvalQuestions.objects.all()


    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})

def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})

'''
HELPER METHODS
'''
def professorsSearch(searchQuery, searchPOST):
    dataObjects = EvalResults.objects.all()
    lastname = dataObjects.filter(instr_last_name__in= searchQuery) #search by last name
    firstname = dataObjects.filter(instr_first_name__in=searchQuery) #search by first name
    startsL = dataObjects.filter(instr_last_name__istartswith=searchPOST) #search by beginning of last name
    startsF = dataObjects.filter(instr_first_name__istartswith=searchPOST) #search by beginning of first name
    #combine results from search methods above
    results = lastname | firstname | startsL | startsF

    foundProfs = set()
    #sets to prevent duplicate results
    seenP = set()
    for result in results:
        seenC = set()
        if result.instr_full_name not in seenP:
            seenP.add(result.instr_full_name)
            p = Professor(result.instr_first_name, result.instr_last_name)
            #Find courses that this professor teaches
            myCourse = results.filter(instr_first_name=result.instr_first_name,
                                      instr_last_name=result.instr_last_name)
            for c in myCourse:
                if c.class_desc not in seenC:
                    seenC.add(c.class_code)
                    p.addCourse(Course(c.class_code, c.class_subj, str(c.class_number)))

            p.setCommonCourse()
            foundProfs.add(p)
    return foundProfs

def coursesSearch(searchQuery, searchPOST):
    seenC = set() #prevent duplicate tiles
    dataObjects = EvalResults.objects.all()
    fullName = dataObjects.filter(class_code__contains=searchPOST) #search by readable name
    #separate lists because django throws a value error if you try to
    #lookup an integer database field in a list containing strings and vice versa
    subjects = list()
    numbers = list()
    #split up results in course-number format into a separate
    #list that can be used for querying the data
    for item in searchQuery:
        if '-' in item:
            subjectNumber = item.split('-')
            if len(subjectNumber) >= 2:
                try:
                    subjects.append(str(subjectNumber[0]))
                    numbers.append(int(subjectNumber[1]))
                except ValueError:
                    continue

    subjNum = dataObjects.filter(class_subj__in=subjects, class_number__in=numbers) #search by subject-number
    if not subjNum.exists():
        subjNum = dataObjects.filter(class_subj__in=searchQuery)

    #combine results from above search method
    results = fullName | subjNum
    foundCourses = list()
    for result in results:
        seenP = set()
        if result.class_code not in seenC:
            seenC.add(result.class_code)
            course = Course(result.class_code, result.class_subj, result.class_number)
            #calculate how many sections there are
            allSections = results.filter(class_subj=result.class_subj, class_number=result.class_number)
            course.numSections = allSections.count()
            #Find campuses course is offered in
            for section in allSections:
                course.campus.add(section.campus)
            #Find professors who teach this course
            myProfessor = results.filter(class_subj=result.class_subj,
                                         class_number=result.class_number)
            for prof in myProfessor:
                if prof.instr_full_name not in seenP:
                    seenP.add(result.instr_full_name)
                    course.addProfessor(Professor(prof.instr_first_name, prof.instr_last_name))
            foundCourses.append(course)
    return foundCourses
