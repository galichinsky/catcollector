from django.contrib import admin
from .models import Cat, Feeding, Toy

# Register your models here.

admin.site.register(Cat)
admin.site.register(Feeding) # Register the Feeding model
admin.site.register(Toy) # Register the Toy model
