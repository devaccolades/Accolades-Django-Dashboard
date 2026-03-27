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

class BlogSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()
    class Meta:
        model = Blogs
        fields = ['id', 'title', 'meta_title', 'meta_description', 'image', 'image_alt', 'descriptions', 'slug', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d/%m/%Y")