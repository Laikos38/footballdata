from django.urls import include, path

urlpatterns = [
    path("api/", include("footballdata.api.urls")),
]
