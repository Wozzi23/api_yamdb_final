from api.views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                       GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

v1_router_auth = SimpleRouter()
v1_router = DefaultRouter()

v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories')
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres')
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles')
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='rewiew')
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='commetn')
v1_router_auth.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('auth/token/', APIGetToken.as_view(), name='get_token'),
    path('', include(v1_router_auth.urls)),
    path('', include(v1_router.urls)),
    path('auth/signup/', APISignup.as_view(), name='signup'),
]
