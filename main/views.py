from django.shortcuts import render
from django.shortcuts import render_to_response

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')
    
def search(request):
    if request.method == 'POST':
        data = request.POST["search"]
        result = list()
        result.append("This is for testing")
        result.append("You searched for: " + data)
        return render(request, 'main/search.html', {'result': result})
    else:
        return render(request, 'main/search.html')

def professor(request, lastname, firstname):
    return render_to_response('main/professor.html', {'firstname': firstname,'lastname':lastname})
    
def course(request, coursecode, coursenumber):
    return render_to_response('main/course.html', {'coursecode': coursecode,'coursenumber':coursenumber})
