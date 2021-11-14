from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics, permissions, status, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from filters.user_filter import UserFilter
from serializers import serializers
from serializers.serializers import UserSerializer
from accounts.models import UserProfile

from django_filters import rest_framework as filters

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
        except:
            PermissionDenied

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True) and not user.is_deleted:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied


class UserProfileAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserModify(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, pk, *args, **kwargs):
        user = self.request.user
        if user.pk == pk:
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_access == 1:
            return self.list(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UserDelete(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.is_deleted = True
        user.save()

        return Response("deleted successfully")


class UserLogout(generics.GenericAPIView):
    pass
