from django.shortcuts import get_list_or_404, render
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
    lastname = lastname.title()
    firstname = firstname.title()
    prof = get_list_or_404(EvalResults, instr_last_name=lastname, instr_first_name=firstname)
    
    prof_size = len(prof)

    questions = EvalQuestions.objects.all()
    
    q_ratings = [0] * 10

    # Average question ratings
    for professor in prof:
        q_ratings[0] += professor.q1_average
        q_ratings[1] += professor.q2_average
        q_ratings[2] += professor.q3_average
        q_ratings[3] += professor.q4_average
        q_ratings[4] += professor.q5_average
        q_ratings[5] += professor.q6_average
        q_ratings[6] += professor.q7_average
        q_ratings[7] += professor.q8_average
        q_ratings[8] += professor.q9_average
        q_ratings[9] += professor.q10_average
    for index in range(10):
        q_ratings[index] = round(q_ratings[index] / prof_size, 2)

    # Removes duplicate classes that the professor teaches
    seen = set()
    courses = [x for x in prof if x.class_code not in seen and not seen.add(x.class_code)]

    return render(request, 'main/professor.html', {'firstname': firstname,'lastname':lastname, 'questions': questions, 'ratings': q_ratings, 'courses': courses})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})

