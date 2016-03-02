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
        searchData = request.GET["search"]
        #Create professor set to pass to the template
        data = searchData.split()

        foundProfs = professorsSearch(data)
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
def professorsSearch(searchQuery):
    results = EvalResults.objects.filter(instr_last_name__in= searchQuery) #search by last name
    if(results.exists() == False):
        results = EvalResults.objects.filter(instr_first_name__in=searchQuery) #search by first name

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
    results = EvalResults.objects.filter(class_code__contains=searchPOST) #search by readable name
    if(results.exists() == False):
        results = EvalResults.objects.filter(class_subj__in=searchQuery) #search by course code

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
