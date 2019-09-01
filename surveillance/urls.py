from django.urls import path
from surveillance import views

app_name = 'surveillance'
urlpatterns = [
    path('service/', views.service, name='service'),
    path('upload/', views.upload, name='upload'),
]