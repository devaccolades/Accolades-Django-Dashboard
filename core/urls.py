from django.urls import path
from .views import *

urlpatterns = [
    path("case-studies/", CaseStudyListAPIView.as_view(), name="case-studies"),
    path('seo/', SeoListAPIView.as_view(), name='seo-list'),
    path("seo/<str:name>/", SeoRetrieveAPIView.as_view(), name="seo-detail"),
    path('blogs/', BlogsViewset.as_view(), name='blogs-list'),
    path('blogs/<slug:slug>', BlogsViewset.as_view(), name='get_blog_by_slug'),
]
