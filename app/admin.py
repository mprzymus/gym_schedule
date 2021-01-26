from django.contrib import admin

# Register your models here.
from app.model.models import Exercise, ExerciseUsage, UsersCoach

admin.site.register(Exercise)
admin.site.register(ExerciseUsage)
admin.site.register(UsersCoach)
