from django.urls import path,include
from Master import views
app_name="master"
urlpatterns = [
    path('HomePage/', views.HomePage,name='HomePage'),
    path('Questions/', views.Questions,name='Questions'),
    path('Submit',views.Submit,name='Submit'),
    path('Logout/',views.Logout,name="Logout"),
]
    