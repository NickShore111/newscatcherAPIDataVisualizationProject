from django.urls import path
from . import views
# from newscatcher_api.views import HomeView
app_name = 'newscatcher'
urlpatterns = [ 
    path('', views.index, name='home'),
    # path('results/', views.results, name='results'),
    path('technologies/', views.technologies, name='technologies'),
    path('methods/', views.methods, name='methods'),

]
