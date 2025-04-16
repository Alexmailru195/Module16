from django.contrib import admin
from .models import Breed, Dog

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'owner', 'birth_date')
    list_filter = ('breed', 'owner')
    search_fields = ('name', 'owner__username')