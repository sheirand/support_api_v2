from rest_framework import serializers

from issue.models import Comments, Issue
from user import serializer as user_serializer


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for Issue model"""
    assignee = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_by = user_serializer.UserSerializer(read_only=True)
    updated_by = serializers.CharField(read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"
        ordering = ["-id"]


class IssueStatusSerializer(serializers.ModelSerializer):
    """Serializer for Issue model (for staff)"""
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ['assignee', 'status', "updated_by"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    issue = serializers.CharField(read_only=True)
    created_by = user_serializer.UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"
