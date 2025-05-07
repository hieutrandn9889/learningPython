from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('static/', views.static, name='static'),
    path('variable/', views.variable, name='variable'),
    path('counterGETInput/', views.counterGETInput, name='counterGETInput'),
    path('GETTextarea/', views.GETTextarea, name='GETTextarea'),
    path('POSTTextarea/', views.POSTTextarea, name='POSTTextarea'),
]
