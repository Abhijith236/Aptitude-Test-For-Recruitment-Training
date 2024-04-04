from django.urls import path,include
from User import views
app_name='user'
urlpatterns = [
    path('HomePage/', views.HomePage,name='HomePage'),
    path('Category/', views.Category,name='Category'),
    path('Questions/<int:cid>', views.Questions,name='Questions'),
    path('Test/', views.Test,name='Test'),
    path('PreviousTest/', views.PreviousTest,name='PreviousTest'),
    path('TestQuestions/<int:tid>', views.TestQuestions,name='TestQuestions'),
    path('Logout/', views.Logout,name='Logout'),
]
