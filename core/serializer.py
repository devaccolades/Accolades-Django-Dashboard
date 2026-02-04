from rest_framework import serializers
from .models import CaseStudy


class CaseStudySerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

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
