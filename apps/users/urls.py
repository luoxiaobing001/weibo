from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter

from users.views import BlogViewSet, FollowView, GetNewsFeedView

router = DefaultRouter()
router.register(r'blog', BlogViewSet, base_name='blog')


urlpatterns = [
    # router的path路径
    path('', include(router.urls)),
    path('follow/',FollowView.as_view()),
    path('getNews/',GetNewsFeedView.as_view())
]