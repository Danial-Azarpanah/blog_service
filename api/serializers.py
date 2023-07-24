from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.full_name", read_only=True)
    category = serializers.CharField(source="category.title")

    class Meta:
        model = Post
        exclude = ("id",)

