from rest_framework import viewsets
from registration.serializers import CustomUserSerializer
from .models import Statusapp
from .serializers import StatusappSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Statusapp
from .serializers import StatusappSerializer
from django.shortcuts import get_object_or_404
from registration.models import CustomUser
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from relationship.models import  Follow
from .serializers import StatusappSerializer
def upload_status(request):

    # Get user_id from the request data
    user_id = request.data.get('user_id', None)

    # Check if user_id is provided in the request data
    if user_id is None:
        return Response({'message': 'user_id is required'})

    # Retrieve the user with the provided user_id
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'})

    # Add the user instance to the request data
    request.data['user_id'] = user.id
    request.data['status'] = True
    # Create the serializer with the user instance as user_id
    serializer = StatusappSerializer(data=request.data)
    if serializer.is_valid():
        # Assign the user instance as user_id and save the status
        serializer.save()

        return Response({'message': 'Status uploaded successfully'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_status(request):
    user_id = request.GET.get('user_id')
    status_id = request.GET.get('status_id')

    if user_id is None or status_id is None:
        return Response({'error': 'Missing user_id or status_id query parameters'}, status=400)

    try:
        # Get the status based on the provided status_id
        status = Statusapp.objects.get(id=status_id, user_id=user_id)
        
        # Check if the user making the request is the owner of the status
        if user_id != status.user_id.id:
            return Response({'error': 'You are not authorized to delete this status'}, status=403)

        # Delete the status
        status.delete()

        return Response({'message': 'Status deleted successfully'})
    except Statusapp.DoesNotExist:
        return Response({'error': 'Status not found'}, status=404)

@api_view(['GET'])
def list_statuses(request):
    # Get the user_id from the query parameters
    user_id = request.query_params.get('user_id')

    # Initialize a dictionary to store the results
    statuses_data = {}

    if user_id is not None:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=404)

        # Include statuses of the specified user (user_id)
        user_statuses_query = Statusapp.objects.filter(user_id=user).order_by('-uploaded_at')
        user_statuses_serializer = StatusappSerializer(user_statuses_query, many=True)
        statuses_data['user_statuses'] = user_statuses_serializer.data

        # Include statuses of users you are following, excluding blocked users
        following_users = Follow.objects.filter(follower=user, approved=True).values_list('followed', flat=True)

        for following_user_id in following_users:
            following_user = CustomUser.objects.get(id=following_user_id)

            # Exclude blocked users
            if user not in following_user.blocked_users.all() and following_user not in user.blocked_users.all():
                following_statuses_query = Statusapp.objects.filter(user_id=following_user).order_by('-uploaded_at')
                following_statuses_serializer = StatusappSerializer(following_statuses_query, many=True)
                statuses_data[following_user.name] = following_statuses_serializer.data

    return Response(statuses_data)
@api_view(['GET'])
def list_all_statuses(request):
    # Query all Statusapp objects and order them by the 'uploaded_at' field in descending order
    all_statuses_query = Statusapp.objects.all().order_by('-uploaded_at')
    all_statuses_serializer = StatusappSerializer(all_statuses_query, many=True)

    # Serialize the data and return it as a JSON response
    return Response(all_statuses_serializer.data)
from rest_framework.views import APIView
class UserStatusAPIView(APIView):
    def get(self, request):
        user_id = self.request.query_params.get('user_id')
        try:
            # Check if the user with the provided user_id has a status
            status_exists = Statusapp.objects.filter(user_id=user_id, status=True).exists()

            if not status_exists:
                return Response({'message': 'User has no status'})

            # Retrieve the user with the provided user_id
            user = CustomUser.objects.get(id=user_id)

            # Serialize the user data
            user_serializer = CustomUserSerializer(user)

            return Response(user_serializer.data)

        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'})
from userlist.serializers import CustomuSerializer
class StatusAPIView(APIView):
    def get(self, request):
        try:
            # Get a list of all users with status=True
            users_with_status = CustomUser.objects.filter(statusapp__status=True)

            if not users_with_status.exists():
                return Response({'message': 'No users with status found'})

            # Remove duplicates based on user ID
            unique_users = set()
            unique_users_list = []

            for user in users_with_status:
                if user.id not in unique_users:
                    unique_users.add(user.id)
                    unique_users_list.append(user)

            # Serialize the user data
            user_serializer = CustomuSerializer(unique_users_list, many=True)

            return Response(user_serializer.data)

        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'})
from userlist.serializers import CustomuSerializer


class StatusAPIView(APIView):
    def get(self, request):
        try:
            # Get a list of all users with status=True
            users_with_status = CustomUser.objects.filter(statusapp__status=True)

            if not users_with_status.exists():
                return Response({'message': 'No users with status found'})

            # Remove duplicates based on user ID
            unique_users = set()
            unique_users_list = []

            for user in users_with_status:
                if user.id not in unique_users:
                    unique_users.add(user.id)
                    unique_users_list.append(user)

            # Serialize the user data
            user_serializer = CustomuSerializer(unique_users_list, many=True)

            return Response(user_serializer.data)

        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'})            
