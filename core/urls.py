from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SiteConfigurationView, UserViewSet

router = SimpleRouter()

router.register("users", UserViewSet)

urlpatterns = [
                  path(
                      "configs/",
                      SiteConfigurationView.as_view(),
                      name="configs",
                  )
              ] + router.urls
