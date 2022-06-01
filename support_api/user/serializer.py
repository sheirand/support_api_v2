from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User


class StaffSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(raw_password=password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ["id", "first_name",
                  "last_name", "email",
                  "password", "is_staff"]


class UserSerializer(StaffSerializer):
    is_staff = serializers.BooleanField(default=False, read_only=True)
