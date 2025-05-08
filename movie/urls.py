from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('comments', views.CommentViewSet)
router.register('actors', views.ActorViewSet)
router.register('directors', views.DirectorViewSet)
router.register('countries', views.CountryViewSet)
router.register('genres', views.GenreViewSet)

router.register('films', views.FilmViewSet, basename='films')
films_router = routers.NestedSimpleRouter(router, r'films', lookup='film')
films_router.register(r'comments', views.CommentNestedViewSet, basename='film-comments')
films_router.register(r'links', views.LinkNestedViewSet, basename='film-links')

urlpatterns = [
                  path('collections/', views.collection_list),
                  path('collections/<id>/', views.CollectionDetail.as_view()),
                  path('links/', views.LinkList.as_view()),
                  path('links/<id>/', views.LinkDetail.as_view()),
              ] + router.urls + films_router.urls
