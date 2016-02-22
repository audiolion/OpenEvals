from django.shortcuts import get_list_or_404, render
from django.shortcuts import render_to_response
from .models import *

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')
    
def search(request):
    if request.method == 'POST':
        data = request.POST["search"]
        result = EvalResults.objects.filter(instr_first_name__in=data, class_code__in=data)

        return render(request, 'main/search.html', {'result': result})
    else:
        return render(request, 'main/search.html')

def professor(request, lastname, firstname):
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
        q_ratings[index] /= prof_size 

    return render(request, 'main/professor.html', {'firstname': firstname,'lastname':lastname, 'questions': questions, 'ratings': q_ratings})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})
