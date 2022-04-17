from django.urls import path
from . import views

app_name    = "re_QA"
urlpatterns = [
    path('', views.index, name="index"),
]