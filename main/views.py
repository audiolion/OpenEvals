from django.shortcuts import render
from django.shortcuts import render_to_response

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')
    
def search(request):
    return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})
