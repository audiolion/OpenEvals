from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import *
from .Professor import *

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')
    
def search(request):
    if request.method == 'POST':
        data = request.POST["search"]
        results = EvalResults.objects.filter(instr_first_name__in=data, class_code__in=data)
        foundProfs = set()
        for result in results:
            p = Professor(result.instr_first_name, result.instr_last_name)
            myCourse = EvalResults.objects.filter(instr_first_name=result.instr_first_name,
                                                  instr_last_name=result.instr_last_name)
            for c in myCourse:
                p.add([c.class_code, c.class_number])
            foundProfs.add(p)

        return render(request, 'main/search.html', {'professors': foundProfs})
    else:
        return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    prof = EvalResults.objects.filter(instr_last_name=lastname,
                                      instr_first_name=firstname)
    questions = EvalQuestions.objects.all()


    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})

