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

#   blog
class BlogsViewset(APIView):
    
    """
    API view for fetching Blog and Blog Details for users with pagination.
    """
    model = Blogs
    serializers_class = BlogSerializer

    def get(self, request, slug = None):
        try:
            if slug:
                instance = self.get_object(slug)
                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "details": "Error",
                        "message": "Blog not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = BlogSerializer(
                    instance, 
                    context={'request': request}
                )

                related_blogs = self.model.objects.filter(is_deleted=False).exclude(slug=slug)[:3]
                related_serializer = BlogSerializer(
                    related_blogs, 
                    many=True,
                    context={'request': request}
                )
                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "related_blogs": related_serializer.data,
                    "message": "Blog details retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)

            queryset = self.model.objects.filter(is_deleted=False)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            serializer = self.serializers_class(
                    page, 
                    many=True, 
                    context={'request': request}
                )

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "pagination": {
                        "total_items": paginator.page.paginator.count,
                        "total_pages": paginator.page.paginator.num_pages,
                        "current_page": paginator.page.number,
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link()
                    },
                "message" : "Blog's data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Blog's: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Blog's",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get_object(self, slug):
        try:
            return self.model.objects.filter(slug=slug).first()
        except Exception as e:
            logger.error(f"Error retrieving object: {str(e)}")
            return None