from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.auth_login, name='login'),
    path('register', views.registerView, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('step1', views.step1View, name='step1'),
    path('step2', views.step2View, name='step2'),
    path('step3', views.step3View, name='step3'),
]