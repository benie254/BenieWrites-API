from rest_framework import serializers

from benie_app.models import Story, Tag, Chapter, Reaction, Feedback, Reply, Page, Subscriber, Notification, Contact, Poem


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('__all__')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('__all__')

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('__all__')        

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('__all__')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('__all__')

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('__all__')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('__all__')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('__all__')

class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('__all__')

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('__all__')

class DelSubSerializer(serializers.ModelSerializer):
    class Meta:
        model: Subscriber
        fields = ('email',)