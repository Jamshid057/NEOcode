from django.urls import path

from . import views

app_name = "problems"

urlpatterns = [
    path("category/<int:pk>/", views.category_problem_list, name="category"),
    path("problem/<int:pk>/", views.problem_detail, name="detail"),
    path("problem/<int:pk>/submit/", views.problem_submit, name="submit"),
]
