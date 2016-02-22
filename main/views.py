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
    
def search(request):
    if request.method == 'POST':
        searchPOST = request.POST["search"]
        #Create professor set to pass to the template
        data = searchPOST.split()
        results = EvalResults.objects.filter(instr_last_name__in= data) #search by last name
        if(results.exists() == False):
            results = EvalResults.objects.filter(instr_first_name__in=data) #search by first name

        foundProfs = set()
        for result in results:
            p = Professor(result.instr_first_name, result.instr_last_name)
            myCourse = EvalResults.objects.filter(instr_first_name=result.instr_first_name,
                                                  instr_last_name=result.instr_last_name)
            for c in myCourse:
                p.addCourse(Course(c.class_desc, c.class_code, str(c.class_number)))
            p.setCommonCourse()
            foundProfs.add(p)

        #Create course set to pass to the template
        results = EvalResults.objects.filter(class_desc__contains=searchPOST) #search by readable name
        if(results.exists() == False):
            results = EvalResults.objects.filter(class_code__in=data) #search by course code

        foundCourses = set()
        for result in results:
            course = Course(result.class_desc, result.class_code, result.class_number)
            myProfessor = EvalResults.objects.filter(class_code=result.class_code,
                                                     class_number=result.class_number)
            for prof in myProfessor:
                course.addProfessor(Professor(prof.instr_first_name, prof.instr_last_name))
            foundCourses.add(course)

        return render(request, 'main/search.html', {'professors': foundProfs, "courses" : foundCourses})
    else:
        return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    prof = EvalResults.objects.filter(instr_last_name=lastname,
                                      instr_first_name=firstname)
    questions = EvalQuestions.objects.all()


    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})

