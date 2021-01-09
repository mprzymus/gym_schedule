from django.contrib import admin

# Register your models here.
from app.models import Exercise, ExerciseUsage

admin.site.register(Exercise)
admin.site.register(ExerciseUsage)
