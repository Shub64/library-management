# myapp/urls.py  
from django.urls import path  
from .import views  
from django.views.generic import TemplateView 

urlpatterns = [  
    path('', views.Home, name='Home'),  
    path('submit/', views.submit_page, name='submit_data'),  
    path('searchbook/', TemplateView.as_view(template_name='newapp/searchbook.html'), name='searchbook'),
    path('viewbooks/', TemplateView.as_view(template_name='newapp/viewbooks.html'), name='viewbooks'),
    path('issuebook/',TemplateView.as_view(template_name='newapp/issuebook.html'), name='issuebook'),
    path('login/',TemplateView.as_view(template_name='newapp/login.html'), name='login'),
    path('registeration/',TemplateView.as_view(template_name='newapp/registeration.html'), name='registeration'), 
    path('returnbook/', views.returnbook, name='returnbook'),
    path('home1/',TemplateView.as_view(template_name='newapp/home1.html'), name='home1'),
    path('Home/',TemplateView.as_view(template_name='newapp/Home.html'), name='Home'),

]