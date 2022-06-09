from django.urls import path
from . import views

app_name    = "re_QA"
urlpatterns = [
    path('', views.index, name="index"),
    path('single/<uuid:pk>/', views.single, name="single"),
    path('questions/', views.questions, name="questions"),
    path("photo/",views.photo, name="photo"),
    path("document/",views.document, name="document"),
    path("update_question_user/",views.update_question_user, name="update_question_user"),
    path("update_profile/",views.UpdateProfileView.as_view(), name="update_profile"),
    path("create_profile/",views.create_profile, name="create_profile"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name="activate"),
]