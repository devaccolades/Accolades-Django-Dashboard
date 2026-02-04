from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("no", "title", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "category")
