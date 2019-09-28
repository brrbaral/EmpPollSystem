from django.urls import path
from . import views


urlpatterns = [
    path('',views.EmployeeList.as_view(),name='employee_list'),
    path('<int:pk>/details',views.EmployeeDetail.as_view(),name='employee_detail'),
    path('add/',views.employee_add,name='employee_add'),
    path('<int:id>/edit/',views.Employee_edit,name='employee_edit'),
    path('<int:pk>/delete',views.Employee_delete.as_view(),name='employee_delete'),
    path('profile/',views.MyProfile.as_view(),name='my_profile'),
    path('profile/update',views.ProfileUpdate.as_view(),name='update_profile')
]
