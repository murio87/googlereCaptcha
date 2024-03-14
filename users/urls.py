from django.urls import path
from .import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/<username>', views.profile_view, name='profile'),

]