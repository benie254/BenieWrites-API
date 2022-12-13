from django.contrib import admin
from benie_app.models import Story, Tag, Chapter, Reaction

# Register your models here.
admin.site.register(Story)
admin.site.register(Tag)
admin.site.register(Chapter)
admin.site.register(Reaction)
