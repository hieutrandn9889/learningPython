from django.db import models
from django.urls import reverse

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    is_true = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=500)
    link = models.TextField(max_length=500)
    slug = models.SlugField(unique=True, default='default-slug')
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name