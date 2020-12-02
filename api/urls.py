from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowList, GroupList


router = DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='Comment')
router.register('posts', PostViewSet, basename="Post")


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('group/', GroupList.as_view()),
    path('follow/', FollowList.as_view())
]

