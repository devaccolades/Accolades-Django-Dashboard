from django.urls import path
from .views import CaseStudyListAPIView

urlpatterns = [
    path("case-studies/", CaseStudyListAPIView.as_view(), name="case-studies"),
]
