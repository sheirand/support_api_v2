from rest_framework import viewsets, mixins, exceptions
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from user.authentication import CustomUserAuthentication
from issue.models import Issue, Comments
from issue.serializers import IssueSerializer, IssueStatusSerializer, CommentSerializer
from issue.permissions import IsOwnerOrStaff, IsStaff
from user.services import select_user_via_email

class IssueViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomUserAuthentication,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if self.request.user.is_staff:
            if not pk:
                return Issue.objects.all()
            else:
                return Issue.objects.filter(pk=pk)
        else:  # self.request.user.is_authenticated:
            if not pk:
                return Issue.objects.filter(created_by=self.request.user)
            else:
                return Issue.objects.filter(created_by=self.request.user, pk=pk)
#        else:
#           raise exceptions.AuthenticationFailed("Not authorized")

    def get_serializer_class(self):
        if self.action in ['update', 'partially_update',
                           'destroy']:
            serializer_class = IssueStatusSerializer
        else:
            serializer_class = IssueSerializer

        return serializer_class

    def get_permissions(self):

        if self.action == 'retrieve':
            permission_classes = (IsOwnerOrStaff, IsAuthenticated)
        elif self.action in ['update',
                             'partial_update',
                             'perform_update']:
            permission_classes = (IsStaff, IsAdminUser, IsAuthenticated)
        elif self.action == 'destroy':
            permission_classes = (IsAdminUser, IsAuthenticated)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
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
        # if not self.request.user.is_authenticated:
        #     raise exceptions.AuthenticationFailed("Not authorized")
         serializer.save(created_by=self.request.user, issue_id=self.kwargs.get('issue_id'))
