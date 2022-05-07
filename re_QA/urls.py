from django.urls import path
from . import views

app_name    = "re_QA"
urlpatterns = [
    path('', views.index, name="index"),
    path('single/<uuid:pk>/', views.single, name="single"),
    path('questions/', views.questions, name="questions"),
    path("photo/",views.photo, name="photo"),
    path("document/",views.document, name="document"),
    
]