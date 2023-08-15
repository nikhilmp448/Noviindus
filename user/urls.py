from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('password', views.change_password, name='password'),
    path('course', views.course, name='course'),
    path('createcourse', views.create_course, name='createcourse'),
    path('updatecourse/<str:id>/', views.update_course, name='updatecourse'),
    path('deletecourse/<int:id>', views.delete_course, name='deletecourse'),
    
    
]