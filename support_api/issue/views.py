from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from issue.models import Comments, Issue
from issue.permissions import IsOwnerOrStaff, IsStaff
from issue.serializers import (CommentSerializer, IssueSerializer,
                               IssueStatusSerializer)
from issue.tasks import send_notification
from user.authentication import CustomUserAuthentication


class IssueViewSet(viewsets.ModelViewSet):
    """Issue endpoint view"""
    authentication_classes = (CustomUserAuthentication,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if self.request.user.is_staff:
            if not pk:
                return Issue.objects.all()
            return Issue.objects.filter(pk=pk)
        else:
            if not pk:
                return Issue.objects.filter(created_by=self.request.user)
            return Issue.objects.filter(created_by=self.request.user, pk=pk)

    def get_serializer_class(self):
        if self.action in ['update', 'partially_update',
                           'destroy']:
            serializer_class = IssueStatusSerializer
        else:
            serializer_class = IssueSerializer

        return serializer_class

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = (IsOwnerOrStaff,)
        elif self.action in ['update',
                             'partial_update',
                             'perform_update']:
            permission_classes = (IsStaff,)
        elif self.action == 'destroy':
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # email notification if status or assignee is changed
        if serializer.validated_data.get('assignee') and \
                (serializer.validated_data.get('assignee') != instance.assignee):
            send_notification.delay(
                pk=instance.pk,
                assignee=str(serializer.validated_data.get('assignee'))
            )
        if instance.status != serializer.validated_data.get('status'):
            send_notification.delay(
                user_email=str(instance.created_by),
                pk=instance.pk,
                status=serializer.validated_data.get('status')
            )

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """Comments endpoint view"""
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsOwnerOrStaff, IsAuthenticated)
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        pk = self.kwargs.get('pk')
        if not pk:
            return Comments.objects.filter(issue_id=issue_id)
        else:
            return Comments.objects.filter(issue_id=issue_id, pk=pk)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, issue_id=self.kwargs.get('issue_id'))
