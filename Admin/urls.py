from django.urls import path,include
from Admin import views
app_name = "admin"
urlpatterns = [
    path('HomePage/', views.HomePage,name='HomePage'),
    path('AjaxPlace/',views.AjaxPlace,name="AjaxPlace"),

    path('NewDistrict/',views.NewDistrict,name="NewDistrict"),
    path('DeleteDistrict/<int:did>',views.DeleteDistrict,name="DeleteDistrict"),
    path('EditDistrict/<int:eid>',views.EditDistrict,name="EditDistrict"),

    path('NewPlace/',views.NewPlace,name="NewPlace"),
    path('DeletePlace/<int:did>',views.DeletePlace,name="DeletePlace"),
    path('EditPlace/<int:eid>',views.EditPlace,name="EditPlace"),

    path('NewCategory/',views.NewCategory,name="NewCategory"),
    path('DeleteCategory/<int:did>',views.DeleteCategory,name="DeleteCategory"),
    path('EditCategory/<int:eid>',views.EditCategory,name="EditCategory"),


    path('Master/',views.Master,name="Master"),
    path('DeleteMaster/<int:mid>',views.DeleteMaster,name="DeleteMaster"),


    path('Logout/',views.Logout,name="Logout"),
]
