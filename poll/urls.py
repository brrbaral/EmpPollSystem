from django.urls import path
from . import views


urlpatterns = [

    path('',views.IndexView.as_view(),name='polls_list'),
    path('<int:pk>/details',views.Details.as_view(),name='details'),
    path('<int:id>/',views.poll, name='poll_details'),
    path('add/', views.Poll_Add, name='poll_add'),
    path('<int:id>/edit',views.Poll_Edit,name='poll_edit'),
    path('<int:id>/delete',views.Poll_Delete,name='poll_delete')

    #path('<int:id>/edit/', views.PollView.as_view(), name='poll_edit'),
    #path('<int:id>/delete/', views.PollView.as_view(), name='poll_delete'),
]