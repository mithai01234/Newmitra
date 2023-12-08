from django.db.models import Sum
from relationship.models import Follow
from .serializers import VideoSerializer, LikeSerializer, CommentUpdateSerializer, CommentSerializer, \
    VideoUpdateSerializer, CommentDeSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video, Like, Comment, Point
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.conf import settings
from moviepy.editor import VideoFileClip
import os
from registration.models import CustomUser
import moviepy.editor as mp
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.conf import settings
import uuid
from moviepy.editor import VideoFileClip
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Video
from .serializers import VideoSerializer
import moviepy.editor as mp
from PIL import Image
import vultr
import boto3
import os
import uuid
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, status
from rest_framework.response import Response
from moviepy.editor import VideoFileClip
from PIL import Image
from .models import Video
from .serializers import VideoSerializer
import tempfile
import os
import uuid
import tempfile
import boto3
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
  # Replace 'your_app' with your actual app name
from django.core.files.base import ContentFile
from PIL import Image
import io
import os
import uuid
import tempfile
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import boto3
from storages.backends.s3boto3 import S3Boto3Storage
from rest_framework.response import Response
from rest_framework import status
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)

        if serializer. is_valid():
            video_file = request.data.get('file')
            title = request.data.get('title', '')



            if not video_file:
                return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Initialize the S3 client for Vultr Object Storage
                s3 = boto3.client(
                    's3',
                    endpoint_url='https://blr1.vultrobjects.com',  # Vultr Object Storage endpoint
                    aws_access_key_id='RPXXFVF2T8NYMS0HU92G',
                    aws_secret_access_key='nU3jO0rP7pCGKFmab3vUuSDacaaN4jvKlOlFCMHM'
                )

                # Use the original file name as the key for the video file within the 'videos' directory
                video_key = f'videos/{video_file.name}'

                # Save the video directly to Vultr Object Storage
                video_data = video_file.read()

                s3.upload_fileobj(io.BytesIO(video_data), 'mitra-bucket', video_key)

                # Generate a thumbnail from the video and save it
                thumbnail_path = self.generate_and_save_thumbnail(video_data)

                if thumbnail_path:
                    # Generate a unique key for the thumbnail file within the 'videos' directory
                    thumbnail_key = f'videos/{video_file.name}.thumbnail.jpg'

                    # Upload the thumbnail image directly to Vultr Object Storage
                    thumbnail_data = open(thumbnail_path, 'rb').read()

                    s3.upload_fileobj(io.BytesIO(thumbnail_data), 'mitra-bucket', thumbnail_key)

                    # Save the video data to the database, including the video and thumbnail keys
                    serializer.save(file=video_key, thumbnail=thumbnail_key, status=True)

                    # Clean up temporary files
                    os.remove(thumbnail_path)

                    return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Thumbnail generation failed'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_and_save_thumbnail(self, video_data):
        try:
            # Load the video using MoviePy
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
                temp_video_file.write(video_data)

            video = mp.VideoFileClip(temp_video_file.name)

            # Generate the thumbnail from the first frame of the video
            thumbnail = video.get_frame(0)

            # Create a temporary file to save the thumbnail
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_thumbnail_file:
                thumbnail_image = Image.fromarray(thumbnail)
                thumbnail_image.save(temp_thumbnail_file.name)

                return temp_thumbnail_file.name
        except Exception as e:
            # Handle any errors that may occur during thumbnail creation
            print(f"Thumbnail creation error: {str(e)}")
            return None
    def save_uploaded_video(self, uploaded_video):
        try:
            # Create a FileSystemStorage instance for saving the uploaded video
            fs = FileSystemStorage()

            # Generate a unique temporary file name
            temporary_video_name = fs.get_available_name("temp_video.mp4")

            # Save the uploaded video to the temporary location
            temporary_video_path = fs.save(temporary_video_name, uploaded_video)

            # Get the full file path of the saved temporary video
            return os.path.join(settings.MEDIA_ROOT, temporary_video_path)
        except Exception as e:
            # Handle any errors that may occur during video saving
            print(f"Video saving error: {str(e)}")
            return None

    def compress_video(self, video_path):
        try:
            # Load the video using MoviePy
            video = mp.VideoFileClip(video_path)

            # Define the output file path for the compressed video
            compressed_video_path = "compressed_video.mp4"

            # Define the target resolution and bitrate (adjust as needed)
            # target_resolution = (640, 360)
            original_width, original_height = video.size

            target_bitrate = "500k"

            # Resize the video to the target resolution
            resized_video = video.resize((original_width, original_height))

            # Write the compressed video to the output file with the specified bitrate
            resized_video.write_videofile(compressed_video_path, codec="libx264", bitrate=target_bitrate)

            return compressed_video_path
        except Exception as e:
            # Handle any errors that may occur during video compression
            print(f"Video compression error: {str(e)}")
            return None

    def get_queryset(self):
        # Get the user ID from the URL parameter (e.g., /api/videos/?user_id=123)
        user_id = self.request.query_params.get('user_id')#only these line will get the params
        hello = Video.objects.all()
        hello = hello.order_by('-uploaded_at')
        # Filter videos by the user ID if it's provided in the query parameter
        if user_id is not None:
            queryset = Video.objects.filter(user_id=user_id)

            # Sort the queryset by the last uploaded date in descending order (newest first)
            queryset = queryset.order_by('-uploaded_at')

            return queryset
        else:
            # If user_id is not provided, return all videos
            return hello



            @action(detail=True, methods=['post'])
            def like(self, request, pk=None):
                video = self.get_object()
                user = request.user
                # Check if the user has already liked the video
                existing_like = Like.objects.filter(user=user, video=video).first()
                if existing_like:
                    # Unlike the video if the user has already liked it
                    existing_like.delete()
                    return Response({"message": "Video unliked successfully"}, status=status.HTTP_200_OK)
                else:
                    # Like the video
                    Like.objects.create(user=user, video=video)
                    return Response({"message": "Video liked successfully"}, status=status.HTTP_201_CREATED)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['post'])  # Set detail to False
    def toggle_like(self, request):
        user_id = request.data.get('user_id')
        video_id = request.data.get('video_id')

        user = get_object_or_404(get_user_model(), pk=user_id)
        video = get_object_or_404(Video, pk=video_id)

        existing_like = Like.objects.filter(user=user, video=video).first()

        if existing_like:
            existing_like.delete()
            message = "Video unliked."
        else:
            Like.objects.create(user=user, video=video, is_like=True)
            message = "Video liked."

        return Response({"message": message}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def like_count(self, request, video_pk=None):
        video_id = request.query_params.get('video_id')

        video = get_object_or_404(Video, pk=video_id)

        likes = Like.objects.filter(video=video, is_like=True)
        like_data = [{'username': like.user.name,'uid':like.user.id} for like in likes]

        return Response({"like_count": len(like_data), "likes": like_data}, status=status.HTTP_200_OK)
# Create your views here.
from django.db.models import Sum

class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        # Get the user ID from the URL parameter (e.g., /api/videos/?user_id=123)
        user_id = self.request.query_params.get('user_id')

        hello = Video.objects.all()
        hello = hello.order_by('-uploaded_at')

        # Filter videos by the user ID if it's provided in the query parameter
        if user_id is not None:
            queryset = Video.objects.filter(user_id=user_id)

            # Sort the queryset by the last uploaded date in descending order (newest first)
            queryset = queryset.order_by('-uploaded_at')

            user_share_count = queryset.aggregate(Sum('share_count'))['share_count__sum'] or 0

            # Retrieve follower and following counts for the user
            follower_count = Follow.objects.filter(followed=user_id, approved=True).count()
            following_count = Follow.objects.filter(follower=user_id, approved=True).count()

            # Count the number of likes for the user's videos
            user_like_count = Like.objects.filter(user=user_id, is_like=True).count()

            # Iterate through the videos and check criteria to award points
            for video in queryset:
                user = video.user_id
                try:
                    point = Point.objects.get(user=user)
                except Point.DoesNotExist:
                    point = Point(user=user)

                if (
                    point.is_share == 0 and
                    user_share_count >= 1000 and
                    user_like_count >= 1000 and
                    follower_count >= 1000 and
                    following_count >= 1000
                ):
                    point.points += 5
                    point.is_share = 1
                elif (
                    point.is_share == 1 and
                    user_share_count >= 5000 and
                    user_like_count >= 5000 and
                    follower_count >= 5000 and
                    following_count >= 5000
                ):
                    point.points += 20
                    point.is_share = 2




                elif (
                    point.is_share == 2 and
                    user_share_count >= 10000 and
                    user_like_count >= 10000 and
                    follower_count >= 10000 and
                    following_count >= 10000
                ):
                    point.points += 35
                    point.is_share = 3
                elif (
                    point.is_share == 3 and
                    user_share_count >= 25000 and
                    user_like_count >= 25000 and
                    follower_count >= 25000 and
                    following_count >= 25000
                ):
                    point.points += 60
                    point.is_share = 4
                elif (
                    point.is_share == 4 and
                    user_share_count >= 50000 and
                    user_like_count >= 50000 and
                    follower_count >= 50000 and
                    following_count >= 50000
                ):
                    point.points += 100
                    point.is_share = 5
                elif (
                    point.is_share == 5 and
                    user_share_count >= 100000 and
                    user_like_count >= 100000 and
                    follower_count >= 100000 and
                    following_count >= 100000
                ):
                    point.points += 210
                    point.is_share = 6
                elif (
                    point.is_share == 6 and
                    user_share_count >= 1000000 and
                    user_like_count >= 1000000 and
                    follower_count >= 1000000 and
                    following_count >= 1000000
                ):
                    point.points += 450
                    point.is_share = 7
                elif (
                    point.is_share == 7 and
                    user_share_count >= 5000000 and
                    user_like_count >= 5000000 and
                    follower_count >= 5000000 and
                    following_count >= 5000000
                ):
                    point.points += 1000
                    point.is_share = 8
                elif (
                    point.is_share == 8 and
                    user_share_count >= 10000000 and
                    user_like_count >= 10000000 and
                    follower_count >= 10000000 and
                    following_count >= 10000000
                ):
                    point.points += 2250
                    point.is_share = 9
                elif (
                    point.is_share == 9 and
                    user_share_count >= 100000000 and
                    user_like_count >= 100000000 and
                    follower_count >= 100000000 and
                    following_count >= 100000000
                ):
                    point.points += 5000
                    point.is_share = 10


                point.save()

            return queryset
        else:
            return hello




class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')

        parent_comment_id = self.request.data.get('parent_comment')
        video_id = self.request.data.get('video')
        serializer.save(
            user_id=user_id,
            video_id=video_id,
            parent_comment_id=parent_comment_id,
        )




class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        video_id = self.kwargs['video_id']
        parent_comment_id = self.kwargs.get('parent_comment_id')
        queryset = Comment.objects.filter(video__id=video_id, parent_comment=parent_comment_id).order_by('timestamp')
        return queryset
class ReplyCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        parent_comment_id = self.request.query_params.get('parent_comment_id', None)

        if parent_comment_id is None:
            return Comment.objects.none()

        queryset = Comment.objects.filter(parent_comment=parent_comment_id).order_by('timestamp')
        return queryset

    def list(self, request, *args, **kwargs):
        parent_comment_id = self.request.query_params.get('parent_comment_id', None)

        if parent_comment_id is None:
            return Response({'error': 'parent_comment_id is required as a query parameter'}, status=400)

        queryset = self.get_queryset()
        reply_count = queryset.count()

        serializer = self.get_serializer(queryset, many=True)
        return Response({'replies': serializer.data, 'reply_count': reply_count})

class CommentCountView(generics.RetrieveAPIView):
    def retrieve(self, request):
        video_id = request.query_params.get('video_id', None)

        if video_id is None:
            return Response({'error': 'video_id is required as a query parameter'}, status=400)
        def get_comment_data(comment):
            # Get the comment data
            comment_data = {
                'id':comment.id,
                'user_id':comment.user.id,
                'username': comment.user.name,
                'text': comment.text,
            }

            # Get the replies to this comment
            replies = Comment.objects.filter(parent_comment=comment)
            reply_data = []

            for reply in replies:
                # Recursively get data for each reply
                reply_data.append(get_comment_data(reply))

            if reply_data:
                comment_data['replies'] = reply_data

            return comment_data

        # Count top-level comments (comments without parents) for the video
        top_level_comments = Comment.objects.filter(video__id=video_id, parent_comment__isnull=True)
        comment_count = top_level_comments.count()

        # Count replies for the video
        reply_count = Comment.objects.filter(video__id=video_id, parent_comment__isnull=False).count()

        # Calculate the total comment count as the sum of top-level comments and replies
        total_comment_count = comment_count + reply_count


        # Get comments and their associated replies
        comment_data = []

        for comment in top_level_comments:
            comment_data.append(get_comment_data(comment))

        response_data = {
            'video_id': video_id,
            'comment_count': total_comment_count,  # Use the calculated total comment count
            'comments': comment_data,

        }

        return Response(response_data)

class CommentEditView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

    def patch(self, request, *args, **kwargs):
        comment_id = request.query_params.get('comment_id')
        parent_comment_id = request.query_params.get('parent_comment_id', None)

        if comment_id is not None:
            try:
                if parent_comment_id is not None:
                    # Editing a reply
                    comment = Comment.objects.get(id=comment_id, parent_comment=parent_comment_id)

                else:
                    # Editing a top-level comment
                    comment = Comment.objects.get(id=comment_id)
                serializer = self.get_serializer(comment, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'comment_id is required to edit a comment'}, status=status.HTTP_400_BAD_REQUEST)
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        comment_id = request.query_params.get('comment_id')

        if comment_id is not None:
            try:
                comment = Comment.objects.get(id=comment_id)
                comment.delete()
                return Response({'message': 'Comment deleted successfully'})
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found'})
        else:
            return Response({'error': 'comment_id is required to delete a comment'}, status=status.HTTP_BAD_REQUEST)





class VideoShareView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoUpdateSerializer

    def update(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        user_id = request.data.get('user_id')

        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

        video.share_count += 1
        # Optionally, you can associate this action with the user.
        # Assuming you have a 'shared_by' field in your model.
        # video.shared_by.add(user_id)  # Modify this based on your model structure.

        video.save()
        response_data = {
            'share_count': video.share_count
        }
        return Response({'message': 'Video share count incremented successfully.',**response_data}, status=status.HTTP_200_OK)

class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
      # You can define your own permission class here if needed

    def destroy(self, request, *args, **kwargs):
        video_id = request.query_params.get('video_id')

        if video_id is not None:
            try:
                video = Video.objects.get(id=video_id)
                video.delete()
                return Response({"message": "Video deleted successfully"}, status=204)
            except Video.DoesNotExist:
                return Response({"error": "Video not found"}, status=404)
        else:
            return Response({"error": "Video ID is required as a query parameter"}, status=400)

class GetVideoLink(APIView):
    def get(self, request):
        video_title = request.query_params.get('id')

        if not video_title:
            return Response({'error': 'Id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(pk=video_title)
            video_link = request.build_absolute_uri(settings.MEDIA_URL + video.file.name)
            return Response({'video_link': video_link}, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)


from django.http import JsonResponse


class GetVideoInfoView(APIView):
    def get(self, request):
        video_id = self.request.query_params.get('video_id')

        if video_id is not None:
            try:
                video = Video.objects.get(id=video_id)
                user_name = video.user_id.name
                user_profile_photo = video.user_id.profile_photo.url
                description = video.description
                id=video.user_id.id

                response_data = {
                    'user_name': user_name,
                    'user_profile_photo': user_profile_photo,
                    'description': description,
                    'user_id':id
                }

                return JsonResponse(response_data)
            except Video.DoesNotExist:
                return JsonResponse({'error': 'Video not found'}, status=404)
        else:
            return JsonResponse({'error': 'Video ID is required as a query parameter'}, status=400)
class PerformanceIncomeAPI(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if user_id is None:
            return Response({'error': 'user_id query parameter is missing'})

        if user_id is None:
            return Response({'error': 'user_id query parameter is missing'})

        try:
            user_points = Point.objects.filter(user_id=user_id)
            total_points = user_points.aggregate(total_points=Sum('points'))['total_points']

            # Fetch the total_amount from the user
            user = CustomUser.objects.get(id=user_id)
            total_amount = user.total_amount

            if total_points is not None:
                total_amount += total_points

            response_data = {
                'performance_income': total_points or 0,
                'total_amount': total_amount,
            }

            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)})
class CommentDetailsView(generics.RetrieveAPIView):
    serializer_class = CommentDeSerializer

    def get_queryset(self):
        comment_id = self.request.query_params.get('comment_id', None)
        if comment_id is not None:
            return Comment.objects.filter(id=comment_id)
        else:
            return Comment.objects.none()  # Return an empty queryset if comment_id is not provided

    def get(self, request, *args, **kwargs):
        comment_id = request.query_params.get('comment_id', None)
        if comment_id is None:
            return Response({'error': 'comment_id is required as a query parameter'}, status=400)

        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        else:
            return Response({'error': 'Comment not found'}, status=404)
