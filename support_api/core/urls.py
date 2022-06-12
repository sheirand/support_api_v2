from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from issue.views import CommentsViewSet, IssueViewSet
from user.views import (LoginAPIView, LogoutAPIView, RegisterAPIView,
                        UserAPIView)

router_issue = DefaultRouter()
router_issue.register('issue', IssueViewSet, basename="Issue")
router_issue.register('user', RegisterAPIView, basename="Register")

router_comment = DefaultRouter()
router_comment.register('comment', CommentsViewSet, basename="Comment")

schema_view = get_schema_view(
    openapi.Info(
        title="Support API",
        default_version='v1',
        description="API for Tech Support Sevice",
        contact=openapi.Contact(email="eugene.osakovich@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/login/', LoginAPIView.as_view()),
    path('api/v1/user/logout/', LogoutAPIView.as_view()),
    path('api/v1/user/session/', UserAPIView.as_view({'get': 'list'})),
    path('api/v1/', include(router_issue.urls)),
    path('api/v1/issue/<int:issue_id>/', include(router_comment.urls)),
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-support-api'),
]
