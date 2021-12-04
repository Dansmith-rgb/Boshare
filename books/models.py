from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=True, default="Book")
    author = models.CharField(max_length=200, null=True, default="author")
    publisher = models.CharField(max_length=200, null=True, default="Publisher")
    image = models.URLField(null=True, blank=True, default=None)
    description = models.CharField(default="description", null=True)
    published_date = models.DateField(null=True, blank=True)
    page_count = models.IntegerField(null=True, default=2, blank=True)
    google_book_id = models.CharField(null=True)
    category = models.CharField(default="category", null=True)
    language = models.CharField(default="en", null=True)
    buy_link = models.URLField(null=True)
    ISBN_13 = models.CharField(null=True, blank=True)
