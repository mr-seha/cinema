from core.views import UserViewSet
from movie.urls import router

router.register('users', UserViewSet)

urlpatterns = router.urls
