from django.urls import path
from tasks.views import dashboard,add_task,user_login,register,user_logout , edit_task, delete_task
urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('add_task/',add_task,name='add_task'),
    path('login/',user_login,name='login'),
    path('register/',register,name='register'),
    path('logout/',user_logout,name='logout'),
    path('edit/<int:id>/',edit_task,name='edit_task'),
    path('delete/<int:id>/',delete_task,name='delete_task'),
    
]
