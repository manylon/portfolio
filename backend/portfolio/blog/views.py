from .models import BlogPost
from .serializers import BlogPostListSerializer
from rest_framework import generics


class BlogListView(generics.ListAPIView):
    http_method_names = ['get']
    queryset = BlogPost.objects.all().filter(published=True)
    serializer_class = BlogPostListSerializer
    lookup_field = 'slug'


# class BlogDetailView(generics.RetrieveAPIView):
#     http_method_names = ['get']
#     queryset = BlogPost.objects.all().filter(published=True)
#     serializer_class = BlogPostSerializer
#     lookup_field = 'slug'
