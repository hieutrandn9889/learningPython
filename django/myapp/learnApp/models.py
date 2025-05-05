from django.db import models

class Feature(models.Model):
    id = models.AutoField(primary_key=True)
    is_true = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=500)

    def __str__(self):
        return self.name