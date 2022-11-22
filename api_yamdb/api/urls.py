from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoriesViewSet,
    GenresViewSet,
    JWTTokenViewSet,
    SignUp,
    TitlesViewSet,
    UsersViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"categories", CategoriesViewSet)
router.register(r"genres", GenresViewSet)
router.register(r"titles", TitlesViewSet)
router.register(r"users", UsersViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", SignUp.as_view()),
    path("v1/auth/token/", JWTTokenViewSet.as_view()),
]
