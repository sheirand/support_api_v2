from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from user.authentication import CustomUserAuthentication
from user import services
from user.models import User
from user.serializer import UserSerializer, StaffSerializer
from rest_framework import mixins, views, exceptions, response


class RegisterAPIView(mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = (CustomUserAuthentication,)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return StaffSerializer
        return UserSerializer


class LoginAPIView(views.APIView):

    def get(self, request):
        return response.Response(services.REQUIRED_FIELDS, status=200)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise exceptions.ValidationError(detail=services.REQUIRED_FIELDS)

        user = services.select_user_via_email(email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.create_jwt_token(user_id=user.id)

        resp = response.Response({f"Success": f"You are authenticated as {email}"}, status=200)

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserAPIView(mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.filter(email=self.request.user.email)
        return queryset


class LogoutAPIView(views.APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"Logout": "goodbye!"}
        return resp
