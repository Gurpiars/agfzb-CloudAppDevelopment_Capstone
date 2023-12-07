from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel

# Register your models here.
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display for adding CarModel objects

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'des')
    inlines = [CarModelInline]

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealer_id', 'carmake', 'year', 'type')
