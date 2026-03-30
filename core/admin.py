from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django import forms
# from unfold.contrib.forms.widgets import WysiwygWidget
# from ckeditor.widgets import CKEditorWidget
from django.contrib.admin import ModelAdmin

@admin.register(CaseStudy)
class CaseStudyAdmin(ModelAdmin):
    list_display = ("no", "title", "category",)
    list_filter = ("category",)
    search_fields = ("title", "category")

@admin.register(Seo)
class SeoAdmin(ModelAdmin):

    fieldsets = (
        ("SEO", {
            "classes": ("tab-seo",),
            "fields": ("page", "meta_title", "meta_description"),
        }),
        ("Open Graph", {
            "classes": ("tab-og",),
            "fields": ("og_image", "og_title", "og_description"),
        }),
    )

    tabs = [
        ("SEO", "tab-seo"),
        ("OG Tags", "tab-og"),
    ]

@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Blogs)
class BlogsAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'date_added', )
    search_fields = ('title', 'slug', 'description')
    list_display = ['title', 'author_name', 'date_added']
    prepopulated_fields = {'slug': ('title',)}


