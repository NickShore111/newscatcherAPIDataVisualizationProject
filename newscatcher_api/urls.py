from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='newscatcher-index'),
    path('results/', views.results, name='newscatcher-results'),
    path('display/', views.display, name='newscatcher-display'),
    path('technologies/', views.technologies, name='newscatcher-technologies'),
    path('methods/', views.methods, name='newscatcher-methods'),

]