from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import CaseStudy
from .serializers import CaseStudySerializer


class CaseStudyListAPIView(ListAPIView):
    serializer_class = CaseStudySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CaseStudy.objects.filter(is_active=True)

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by("no")
