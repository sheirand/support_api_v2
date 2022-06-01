from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ["id", "first_name",
                  "last_name", "email",
                  "password", "is_staff"]


# class UserSerializer2(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField(
#         validators=[
#             UniqueValidator(
#                 queryset=User.objects.all()
#             )
#         ]
#     )
#     password = serializers.CharField(write_only=True)
#     is_staff = serializers.BooleanField(default=False, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ["id", "first_name",
#                   "last_name", "email",
#                   "password", "is_staff"]
