from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
]
