from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
# from .models import CaseStudy
# from .serializers import CaseStudySerializer
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status


class CaseStudyListAPIView(ListAPIView):
    serializer_class = CaseStudySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CaseStudy.objects.all()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by("no")


class SeoListAPIView(APIView):
    serializer_class = Seoserializer

    def get(self, request):
        seo = Seo.objects.all()
        serializer = self.serializer_class(seo, many=True,context={"request": request})
        return Response(serializer.data)


class SeoRetrieveAPIView(APIView):
    serializer_class = Seoserializer

    def get(self, request, name):
        """Retrieve a single university by id."""
        seo= get_object_or_404(Seo, page=name)
        serializer = self.serializer_class(seo, context={"request": request})
        return Response(serializer.data)

class BlogCategoryListAPIView(APIView):
    def get(self, request):
        try:
            categories = BlogCategory.objects.all()

            serializer = BlogCategorySerializer(
                categories,
                many=True,
                context={"request": request}
            )

            return Response({
                "StatusCode": 6000,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("ERROR:", str(e))
            return Response({
                "StatusCode": 6002,
                "message": "Failed to fetch categories",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BlogsViewset(APIView):
    model = Blogs
    serializer_class = BlogSerializer

    def get(self, request, slug=None):
        try:
            # ================= BLOG DETAIL =================
            if slug:
                instance = self.get_object(slug)

                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "message": "Blog not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = self.serializer_class(
                    instance,
                    context={'request': request}
                )

                # ✅ RELATED BLOGS FIX
                related_blogs = self.model.objects.filter(
                    selectCategory=instance.selectCategory
                ).exclude(slug=slug)[:3]

                related_serializer = self.serializer_class(
                    related_blogs,
                    many=True,
                    context={'request': request}
                )

                return Response({
                    "StatusCode": 6000,
                    "data": serializer.data,
                    "related_blogs": related_serializer.data,
                }, status=status.HTTP_200_OK)

            # ================= BLOG LIST =================
            queryset = self.model.objects.all().order_by("-date_added")

            serializer = self.serializer_class(
                queryset,
                many=True,
                context={'request': request}
            )

            return Response({
                "StatusCode": 6000,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "StatusCode": 6002,
                "message": "Failed to retrieve blogs",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, slug):
        return self.model.objects.filter(slug=slug).first()