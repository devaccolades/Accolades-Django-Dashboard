from rest_framework import serializers
from .models import *


class CaseStudySerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()
    
    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "no",
            "title",
            "category",
            "description",
            "cover",
            "logo",
            "attachment",
        ]

    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_logo(self, obj):
        request = self.context.get("request")
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None
    def get_attachment(self, obj):
        request = self.context.get("request")
        if obj.attachment and request:
            return request.build_absolute_uri(obj.attachment.url)
        return None

class Seoserializer(serializers.ModelSerializer):
    class Meta:
        model = Seo
        fields = "__all__"

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="selectCategory.name",
        read_only=True
    )

    class Meta:
        model = Blogs
        fields = "__all__"