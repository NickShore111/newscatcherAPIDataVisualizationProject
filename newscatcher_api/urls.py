from django.urls import path
from . import views
from newscatcher_api.views import HomeView

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('refresh', views.refresh, name='refresh'),
    path('results/', views.results, name='results'),
    path('technologies/', views.technologies, name='technologies'),
    path('methods/', views.methods, name='methods'),

]
