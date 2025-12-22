from django.urls import path,include
from category import views

urlpatterns = [
    path("view_category/",views.Categorized.as_view()),
]
