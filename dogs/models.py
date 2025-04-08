from django.db import models
from django.conf import settings

class Breed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dogs')
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='dogs/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.breed})"