from rest_framework import serializers
from users.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['release', 'content']
