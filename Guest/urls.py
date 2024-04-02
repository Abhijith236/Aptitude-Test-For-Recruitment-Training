from django.urls import path,include
from Guest import views
app_name = "guest"
urlpatterns = [
    path('', views.HomePage,name='HomePage'),
    path('UserRegistration/', views.UserRegistration,name='UserRegistration'),
    path('Login/', views.Login,name='Login'),
]
