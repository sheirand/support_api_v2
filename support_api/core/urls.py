from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from issue.views import CommentsViewSet, IssueViewSet
from user.views import (LoginAPIView, LogoutAPIView, RegisterAPIView,
                        UserAPIView)

router_issue = DefaultRouter()
router_issue.register('issue', IssueViewSet, basename="Issue")
router_issue.register('user', RegisterAPIView, basename="Register")

router_comment = DefaultRouter()
router_comment.register('comment', CommentsViewSet, basename="Comment")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/login/', LoginAPIView.as_view()),
    path('api/v1/user/logout/', LogoutAPIView.as_view()),
    path('api/v1/user/session/', UserAPIView.as_view({'get': 'list'})),
    path('api/v1/', include(router_issue.urls)),
    path('api/v1/issue/<int:issue_id>/', include(router_comment.urls)),
]
