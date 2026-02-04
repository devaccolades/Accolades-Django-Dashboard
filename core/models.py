from django.db import models


class CaseStudy(models.Model):
    CATEGORY_CHOICES = [
        ("Real Estate", "Real Estate"),
        ("Interiors", "Interiors"),
        ("Film Industry", "Film Industry"),
    ]

    no = models.PositiveIntegerField(unique=True)

    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    cover = models.ImageField(
        upload_to="case-studies/covers/"
    )

    logo = models.ImageField(
        upload_to="case-studies/logos/",
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["no"]

    def __str__(self):
        return f"{self.no}. {self.title}"

