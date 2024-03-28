from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=500, unique=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('movie_app:products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Movie(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=500, unique=True)
    name = models.CharField(max_length=500)
    desc=models.TextField()
    date=models.DateField()
    img=models.ImageField(upload_to='pics')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cast = models.TextField()
    available = models.BooleanField(default=True)
    trailer_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def __str__(self):
        return self.name

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)



