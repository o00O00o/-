from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('change/', views.change, name='change'),
    path('about/', views.about, name='about'),
]