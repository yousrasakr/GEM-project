from django.db import models

class Statue(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='statue_images/', blank=True, null=True)
    model_3d = models.FileField(upload_to='models_3d/', blank=True, null=True)

    def __str__(self):
        return self.name
