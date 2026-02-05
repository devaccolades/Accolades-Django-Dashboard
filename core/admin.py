from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("no", "title", "category",)
    list_filter = ("category",)
    search_fields = ("title", "category")
