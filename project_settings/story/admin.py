from django.contrib import admin
from .models import Story, Preference, ReadingProgress, DifficultWord


admin.site.register(Story)
admin.site.register(Preference)
admin.site.register(ReadingProgress)
admin.site.register(DifficultWord)

