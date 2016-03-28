from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_list_or_404, render
from django.shortcuts import render_to_response
from django.template  import RequestContext
from django.db.models import Q
from functools import reduce
from itertools import chain
from .models import *
from .Professor import *
from .Course import *
from .forms import SearchForm
import json

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def search(request, searchQ):
    if request.method == 'GET' and len(request.GET) > 0:
        form = SearchForm(request.GET)
        if(form.is_valid()):
            if form.cleaned_data['search'].lower() == '': #csrf breaks form length test in prod
                return render(request, 'main/search.html', {'search_form': form})
            searchData = form.cleaned_data['search'].lower()
            data = searchData.split()

            foundProfs = professorsSearch(searchData)
            foundCourses = coursesSearch(data, searchData)
            return render(request, 'main/search.html', {'professors': foundProfs, "courses" : foundCourses, 'search_form' : form },)
        return render(request, 'main/search.html', {'search_form' : form})
    else:
        form = SearchForm()
        if(searchQ != ""):
            #This is solely for running a search via the common course link
            #in a professor tile. Searching via a url not yet supported
            foundCourses = coursesSearch([searchQ], searchQ)
            return render(request, 'main/search.html', {"courses" : foundCourses, 'search_form' : form })
        else:
            return render(request, 'main/search.html', {'search_form' : form })

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
        #q_ratings[6] += professor.q7_average
        #q_ratings[7] += professor.q8_average
        #q_ratings[8] += professor.q9_average
        #q_ratings[9] += professor.q10_average
    for index in range(6):
        q_ratings[index] = round(q_ratings[index] / prof_size, 2)

    # Removes duplicate classes that the professor teaches
    seen = set()
    courses = [x for x in prof if x.subj + x.class_cat_nbr not in seen and not seen.add( x.subj + x.class_cat_nbr)]

    # Get all results for classes this professor teaches
    similar_profs_query = reduce(lambda q,course: q|Q(class_code=course.class_code), courses, Q())
    sim_profs = EvalResults.objects.filter(similar_profs_query).exclude(instr_first_name=firstname)

    # Removes duplicate professors
    prof_seen = set()
    similar_profs = [x for x in sim_profs if x.instr_full_name not in seen and not seen.add(x.instr_full_name)]

    # Creates list of Course objects
    classes = list()
    for course in courses:
        classes.append(create_course(course,firstname,lastname))

    return render(request, 'main/professor.html', {'firstname': firstname,'lastname':lastname, 'questions': questions, 'ratings': q_ratings,'courses': prof,'sim_profs': similar_profs})

def create_course(course, fname, lname):
    c = Course(course.class_code,course.class_subj,course.class_cat_nbr)
    profs = EvalResults.objects.filter(class_subj=course.class_subj, class_number=course.class_number).exclude(instr_last_name=lname)
    for prof in profs:
        p = Professor(prof.instr_first_name, prof.instr_last_name)
        c.addProfessor(p)
        c.numSections = EvalResults.objects.filter(class_subj=course.class_subj, class_number=course.class_number).count()

    return c

def course(request, subj, classcatnbr):
    #coursecode = coursecode.title()
    #coursenumber = coursenumber.title()
    sections = get_list_or_404(EvalResults, class_subj=subj, class_cat_nbr=classcatnbr)

    sections_size = len(sections)

    questions = EvalQuestions.objects.all()

    q_ratings = [0] * 10

    for courseScores in sections:
        q_ratings[0] += courseScores.q1_average
        q_ratings[1] += courseScores.q2_average
        q_ratings[2] += courseScores.q3_average
        q_ratings[3] += courseScores.q4_average
        q_ratings[4] += courseScores.q5_average
        q_ratings[5] += courseScores.q6_average
        #q_ratings[6] += courseScores.q7_average
        #q_ratings[7] += courseScores.q8_average
        #q_ratings[8] += courseScores.q9_average
        #q_ratings[9] += courseScores.q10_average

    for index in range(6):
        q_ratings[index] = round(q_ratings[index] / sections_size, 2)

    return render_to_response('main/course.html', {'subj': subj,'classcatnbr':classcatnbr, 'questions': questions, 'ratings': q_ratings, 'sections': sections})

def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

'''
HELPER METHODS
'''
def professorsSearch(searchPOST):
    dataObjects = EvalResults.objects.all()
    startsFull = dataObjects.filter(instr_full_name__istartswith=searchPOST) #search by first name
    startsL = dataObjects.filter(instr_last_name__istartswith=searchPOST) #search by beginning of last name
    startsF = dataObjects.filter(instr_first_name__istartswith=searchPOST) #search by beginning of first name
    #combine results from search methods above
    results = startsFull | startsL | startsF

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
                    seenC.add(c.class_subj)
                    p.addCourse(Course(c.class_subj, c.class_subj, str(c.class_cat_nbr), c.class_desc))

            p.setCommonCourse()
            foundProfs.add(p)
    return foundProfs

def coursesSearch(searchQuery, searchPOST):
    seenC = set() #prevent duplicate tiles
    dataObjects = EvalResults.objects.all()
    fullName = dataObjects.filter(class_code__istartswith=searchPOST) #search by readable name
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
        subjNum = dataObjects.filter(class_subj__istartswith=searchPOST)

    #combine results from above search method
    results = fullName | subjNum
    foundCourses = list()
    for result in results:
        seenP = set()
        if result.class_subj + result.class_cat_nbr not in seenC:
            seenC.add(result.class_subj + result.class_cat_nbr)
            course = Course(result.class_code, result.class_subj, result.class_cat_nbr, result.class_desc)
            #calculate how many sections there are
            allSections = results.filter(class_subj=result.class_subj, class_cat_nbr=result.class_cat_nbr)
            course.numSections = allSections.count()
            #Find campuses course is offered in
            for section in allSections:
                course.addCampus(section.campus)
            #Find professors who teach this course
            myProfessor = results.filter(class_subj=result.class_subj,
                                         class_cat_nbr=result.class_cat_nbr)
            for prof in myProfessor:
                if prof.instr_full_name not in seenP:
                    seenP.add(result.instr_full_name)
                    course.addProfessor(Professor(prof.instr_first_name, prof.instr_last_name))
            foundCourses.append(course)
    return foundCourses

'''
AUTOCOMPLETE VIEW
'''
def get_results(request):
    if request.is_ajax():
        currSearch = request.GET['term']
        profs = EvalResults.objects.filter(instr_full_name__icontains=currSearch)[:3]
        courses = EvalResults.objects.filter(class_code__istartswith=currSearch)[:3]
        if not courses.exists():
            courses = EvalResults.objects.filter(class_subj__istartswith=currSearch)[:3]
        foundC = []
        foundP = []
        #sets to prevent duplicate results
        seenP = set()
        seenC = set()
        for result in profs:
            if result.instr_full_name not in seenP:
                seenP.add(result.instr_full_name)
                result_json = {}
                result_json['id'] = result.instr_full_name
                result_json['label'] = result.instr_full_name
                result_json['value'] = result.instr_full_name
                foundP.append(result_json)
        for result in courses:
            if result.class_subj + result.class_cat_nbr not in seenC:
                seenC.add(result.class_subj + result.class_cat_nbr)
                result_json = {}
                result_json['id'] = result.class_subj + result.class_cat_nbr
                result_json['label'] = result.class_subj + " - " + result.class_cat_nbr
                result_json['value'] = result.class_subj + " " + result.class_cat_nbr
                foundC.append(result_json)

        found = foundC + foundP
        data = json.dumps(found)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
