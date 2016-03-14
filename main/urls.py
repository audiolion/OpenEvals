from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about', views.about, name='about'),
    url(r'search/(\w*)', views.search, name='search'),
    url(r'professor/(\w+)/(\w+)', views.professor, name='professor_full'), #Professor with parameter
    url(r'instructor/(\w+)/(\w+)', views.professor, name='professor_full1'),
    url(r'teacher/(\w+)/(w+)', views.professor, name='professor_full2'),
    url(r'course/(\w+)/(\w+)', views.course, name='course_full'),
    url(r'class/(\w+)/(\w+)', views.course, name='course_full1'),
    url(r'section/(\w+)/(\w+)', views.course, name='course_full2'),
    url(r'search-autocomplete/', views.get_results, name='search-autocomplete')

]
