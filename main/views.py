from django.shortcuts import render
from django.shortcuts import render_to_response
from itertools import chain
from .models import *
from .Professor import *

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
                p.addCourse(c.class_code + "-" + str(c.class_number))
            foundProfs.add(p)

        #Create course set to pass to the template
        results = EvalResults.objects.filter(class_desc__contains=searchPOST) #search by readable name
        if(results.exists() == False):
            results = EvalResults.objects.filter(class_code__in=data) #search by course code

        return render(request, 'main/search.html', {'professors': foundProfs, "courses" : results})
    else:
        return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    prof = EvalResults.objects.filter(instr_last_name=lastname,
                                      instr_first_name=firstname)
    questions = EvalQuestions.objects.all()


    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})

