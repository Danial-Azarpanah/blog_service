from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from account.models import User
from .models import Post, Category
from .serializers import PostSerializer


class PostListView(APIView):

    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class PostDetailView(APIView):

    def get(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
        except:
            return Response({"Not found": "The corresponding post was not found"},
                            status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(queryset, many=False)
        return Response(serializer.data, status.HTTP_200_OK)


class PostCreateView(APIView):

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["author"] = User.objects.first()
            serializer.validated_data["category"] = Category.objects.get(
                title=serializer.validated_data["category"]['title'])
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
