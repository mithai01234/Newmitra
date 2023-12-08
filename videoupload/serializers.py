from rest_framework import serializers
from .models import Video, Comment, Like


class VideoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_comment_count(self, obj):
        # You can retrieve the comment count for the video object 'obj'
        return Comment.objects.filter(video=obj).count()
class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['share_count']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
from .models import Point

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['points']
class CommentDeSerializer(serializers.ModelSerializer):
    user_profile_photo = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('user_profile_photo', 'user_name')

    def get_user_profile_photo(self, obj):
        return obj.user.profile_photo.url if obj.user.profile_photo else None

    def get_user_name(self, obj):
        return obj.user.name