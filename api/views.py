from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post, Category
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly


class PostListView(APIView):

    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class PostDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
        except:
            return Response({"Not found": "The corresponding post was not found"},
                            status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(queryset, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
        except:
            return Response({"Not found": "The corresponding post was not found"},
                            status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request=self.request, obj=queryset)
        serializer = PostSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.update(queryset, serializer.validated_data)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
        except:
            return Response({"Not found": "The corresponding post was not found"},
                            status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request=self.request, obj=queryset)
        queryset.delete()
        return Response({"Successful": "Deleted the instance successfully!"}, status.HTTP_200_OK)


class PostCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["author"] = request.user
            serializer.validated_data["category"] = Category.objects.get(
                title=serializer.validated_data["category"]['title'])
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
