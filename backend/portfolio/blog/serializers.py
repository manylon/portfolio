from rest_framework import serializers
from .models import BlogPost
from rest_framework.reverse import reverse


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    tag_name = serializers.StringRelatedField(many=True, source='tag')
    # url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = 'title', 'excerpt', 'thumbnail', 'created_at', 'category_name', 'tag_name', 'medium_url'

    # def get_url(self, obj):
    #     request = self.context.get('request')
    #     return reverse('blog-detail', args=[obj.slug], request=request)


# class BlogPostSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.name')
#     tag_name = serializers.StringRelatedField(many=True, source='tag')

#     class Meta:
#         model = BlogPost
#         fields = 'title', 'content', 'image', 'created_at', 'updated_at', 'category_name', 'tag_name'
