from django.contrib import admin
from django.urls import include, path

from root.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView, name="home"),
    path("auth/", include("accounts.urls")),
    path("problems/", include("problems.urls")),
]
