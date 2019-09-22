from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='create_profile'),
    path('groupregister/', views.group_register, name='create_team_information'),
    path('index/', views.index, name='index'),
    path('user_list/',views.UserListView.as_view(),name='user_list'),
    path('people_list/',views.people,name='people'),
    path('search/', views.search_user, name='search'),
    path('search_group/', views.search_group, name='search_group'),
    path('user_detail/<int:pk>',views.update_user_info,name='user_detail'),
    path('team_update/<int:pk>',views.update_group_info,name='team_update'),
    path('delete_group/<int:pk>',views.delete_group,name='delete_group'),
    path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
    path('delete_operator/<int:pk>',views.delete_operator,name='delete_operator'),
    path('create_operator/',views.OperatorCreateView.as_view(),name='create_operator'),
    path('search_operator/',views.search_operator,name='search_operator'),
    path('update_operator/<int:pk>',views.OperatorUpdateView.as_view(),name='update_operator'),
    ]
