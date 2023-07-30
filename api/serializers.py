from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.full_name", read_only=True)
    category = serializers.CharField(source="category.title")

    class Meta:
        model = Post
        exclude = ("id",)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)

        category_title = validated_data.get('category', {}).get('title')
        if category_title is not None:
            try:
                category = Category.objects.get(title=category_title)
                instance.category = category
            except:
                raise ValidationError("Invalid category.")

        instance.save()
        return instance


