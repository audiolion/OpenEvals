from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about', views.about, name='about'),
<<<<<<< HEAD
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'main/logout.html'},  name='logout'),
    url(r'search/(\w*)', views.search, name='search'),
    url(r'professor/([\w|\W]+)/([\w|\W]+)', views.professor, name='professor_full'), #Professor with parameter
    url(r'instructor/([\w|\W]+)/([\w|\W]+)', views.professor, name='professor_full1'),
    url(r'teacher/([\w|\W]+)/([\w|\W]+)', views.professor, name='professor_full2'),
=======
    url(r'browse', views.browse, name='browse'),
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'main/login.html'}, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'main/logout.html'},  name='logout'),
    url(r'search/(\w*)', views.search, name='search'),
    url(r'professor/([\w|\W]+)/([\w|\W]+)/', views.professor, name='professor_full'), #Professor with parameter
    url(r'instructor/([\w|\W]+)/([\w|\W]+)/', views.professor, name='professor_full1'),
    url(r'teacher/([\w|\W]+)/([\w|\W]+)/', views.professor, name='professor_full2'),
>>>>>>> master
    url(r'course/(\w+)/(\w+)', views.course, name='course_full'),
    url(r'class/(\w+)/(\w+)', views.course, name='course_full1'),
    url(r'section/(\w+)/(\w+)', views.course, name='course_full2'),
    url(r'search-autocomplete/', views.get_results, name='search-autocomplete')

]
