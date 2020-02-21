from django.urls import path
import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('info', views.info, name='info'),
]
