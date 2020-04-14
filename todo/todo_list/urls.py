from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('todohome/', views.todohome, name='todohome'),
    path('delete/<list_id>/', views.delete, name='delete'),
    path('cross_off/<list_id>/', views.cross_off, name='cross_off'),
    path('uncross/<list_id>/', views.uncross, name='uncross'),
    path('edit/<list_id>/', views.edit, name='edit'),
]
