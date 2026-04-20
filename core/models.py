from django.db import models
from django.core.files.base import File
from PIL import Image
from io import BytesIO
import os 
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField  
from django.utils.timezone import now

class CaseStudy(models.Model):
    CATEGORY_CHOICES = [
        ("Real Estate", "Real Estate"),
        ("Interiors", "Interiors"),
        ("Film Industry", "Film Industry"),
        ("Serene homestay", "Serene homestay"),
        ("Ed-Tech", "Ed-Tech"),
    ]
    no = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    description = models.TextField()
    cover = models.ImageField(upload_to="case-studies/covers/")
    logo = models.ImageField(upload_to="case-studies/logos/",null=True,blank=True)
    attachment = models.FileField(upload_to="case-studies/files/",null=True,blank=True)
    # is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["no"]

    def __str__(self):
        return f"{self.no}. {self.title}"

class Seo(models.Model):
    page = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    og_image = models.ImageField(upload_to="seo/og/", blank=True, null=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):

        # Save original first to get file path
        super().save(*args, **kwargs)

        if self.og_image:
            original_path = self.og_image.path
            img = Image.open(self.og_image)

            if img.mode != "RGB":
                img = img.convert("RGB")

            # Optional: Resize if very large (uncomment if needed)
            # max_size = (1920, 1920)
            # img.thumbnail(max_size, Image.ANTIALIAS)

            # Save WebP version in memory
            webp_io = BytesIO()
            img.save(webp_io, format='WebP', quality=70, method=6, optimize=True)

            # Generate .webp filename
            original_filename = os.path.basename(self.og_image.name)
            base, _ = os.path.splitext(original_filename)
            new_filename = f"{base}.webp"

            # Replace the image with optimized WebP version
            self.og_image.save(new_filename, File(webp_io), save=False)

            # Remove original file if not WebP
            if os.path.exists(original_path) and not original_path.endswith('.webp'):
                os.remove(original_path)

            # Save the instance again with updated image
            super().save(update_fields=['og_image'])

    class Meta:
        verbose_name_plural = "SEO data"

    def __str__(self):
        return self.page
    
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'BlogCategory'
        verbose_name_plural = 'Blog Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Blogs(models.Model):
    selectCategory = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=255,blank=True, null=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs')
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    descriptions = RichTextField(blank=True, null=True)
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=600, unique=True)
    author_name = models.CharField(max_length=200,null=True, blank=True)
    author_pro_pic = models.FileField(upload_to="blogs/author/", blank=True, null=True)
    blog_date = models.DateField(default=now)
    date_added = models.DateTimeField(db_index=True, default=timezone.now, editable=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ('-date_added',)

    def __str__(self):
        return self.title if self.title else str(self.id)