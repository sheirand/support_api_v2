from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView
from issue.views import IssueViewSet, CommentsViewSet

router_issue = DefaultRouter()
router_comment = DefaultRouter()

router_issue.register('issue', IssueViewSet, basename="Issue")
router_comment.register('comment', CommentsViewSet, basename="Comment")
router_issue.register('user', RegisterAPIView, basename="Register")
router_issue.register('user/session', UserAPIView, basename="Session")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/login', LoginAPIView.as_view()),
    path('api/v1/user/logout', LogoutAPIView.as_view()),
    path('api/v1/', include(router_issue.urls)),
    path('api/v1/issue/<int:issue_id>/', include(router_comment.urls)),
]
