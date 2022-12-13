from rest_framework import serializers

from benie_app.models import Story, Tag, Chapter, Reaction, Feedback


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('__all__')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('__all__')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('__all__')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('__all__')