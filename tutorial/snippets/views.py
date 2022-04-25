import json
import os
import uuid
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters
from .models import Profile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, Dashboard, DashboardEdit, DashboardRead, DashboardFilter, DashboardSearch, Search, \
    Imagee


def get_tokens_for_user(user):
    """
    This function will generate the token manually
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistration(APIView):

    def post(self, request, format=None):
        """
        This function is for user registration
        """
        serializer = UserRegistrationSerializer(data=request.data)
        print("This is my valid serialized data", serializer.is_valid(raise_exception=True))
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):

    def post(self, request, format=None):
        """
        This function is for user login post method
        """
        serializer = UserLoginSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            return Response({'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
            This function will simply view the specific profile based on the request.user
        """
        print("This is what I am trying to doo", request.user.id)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
           This function will simply view change the password of requested profile
        """
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class CRUDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = Dashboard(data=request.data)
        print("This is the requested file to upload", request.FILES['image'])

        if serializer.is_valid():
            serializer.save(
                user=request.user,
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
            This function is simple get request to view the data according to respective profile
        """

        data = Profile.objects.filter(user=request.user.id)

        print(type(data))
        serializer = DashboardRead(data, many=True)

        data = serializer.data
        profile = Profile()
        if data is None:
            return Response({'msg': 'Data is not present', 'data': data})
        else:
            return Response({'msg': 'Data is following', 'data': data})

    def delete(self, request, instance):
        """
            This function will simply delete the record from the Profile table based on id that is get from the url
        """
        data = Profile.objects.filter(id=instance)
        data.delete()
        if not data:
            return Response({'msg': 'Yes, Your data is deleted successfully '})
        else:
            return Response({'msg': 'Your data is not in the table'})

    def put(self, request, instance):
        """
            This function will simply edit the profile based on the id get from the url.
        """
        try:
            profile = Profile.objects.get(id=instance, user=request.user)
            serializer = DashboardEdit(instance=profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Profile.DoesNotExist as ex:
            return Response({'msg': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'Yes data is updated'}, status=status.HTTP_200_OK)


class Filtering(APIView):
    """
     This is simple filtering view that can give multiple or single result.
    """

    def get(self, request):
        data = Profile.objects.filter(
            Q(nick_name=request.query_params.get('nick_name')) | Q(
                work_description=request.query_params.get('work_description')) | Q(
                Family_detail=request.query_params.get('Family_detail')),
            user=request.user.id)
        serializer = DashboardFilter(data, many=True)
        data = serializer.data

        if data is None:
            return Response({'msg': 'Filter is not able to found', 'data': data})
        else:
            return Response({'msg': 'These are your required data', 'data': data})


class Searching(APIView):
    def get(self, request):
        """
        This is simple search api view that search the required character from the database
        """
        # queryset = Profile.objects.filter(user=request.user).filter(Q(Family_detail__icontains=search)
        #                                          | Q(work_description__icontains=search)
        #                                          | Q(nick_name__icontains=search))

        # family_detail = request.GET.get('Family_detail', None)
        # if family_detail:
        #  queryset = queryset.exclude(~Q(Family_detail__icontains=family_detail))
        search = request.query_params.get('search')
        profile = Profile.objects.filter(Q(Family_detail__icontains=search)
                                         | Q(work_description__icontains=search)
                                         | Q(nick_name__icontains=search))
        serializer = Search(profile, many=True)
        print("This is your required data in the python console", serializer.data)
        data = serializer.data
        if data is None:
            return Response({'msg': 'Filter is not able to found', 'data': data})
        else:
            return Response({'msg': 'These are your required data', 'data': data})


class ImageUpload(APIView):
    pass
