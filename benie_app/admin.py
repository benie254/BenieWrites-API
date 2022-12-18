from django.contrib import admin
from benie_app.models import Story, Tag, Chapter, Reaction, Feedback

# Register your models here.
class StoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('tagged',)
    model = Story
    fields = ['cover','description','title','category','tagged']

admin.site.register(Story,StoryAdmin)
admin.site.register(Tag)
admin.site.register(Chapter)
admin.site.register(Reaction)
admin.site.register(Feedback)
