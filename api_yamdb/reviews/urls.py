from django.urls import include, path
from rest_framework import routers

from .views import RewiewsViewSet

app_name = "rewiews"

router = routers.DefaultRouter()
router.register(r"rewiews", RewiewsViewSet)