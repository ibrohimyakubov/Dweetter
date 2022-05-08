from django.urls import path

from . import views
from .views import dashboard, profile_list, profile

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_func, name='logout'),
]
