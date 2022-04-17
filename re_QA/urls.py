from django.urls import path
from . import views

app_name    = "re_QA"
urlpatterns = [
    path('', views.index, name="index"),
    path("photo/",views.photo, name="photo"),
    path("document/",views.photo, name="document"),
]