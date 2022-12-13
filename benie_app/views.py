from django.shortcuts import render
from benie_app.models import Story, Reaction
from rest_framework.views import APIView
from rest_framework.response import Response

from benie_app.serializers import StorySerializer, TagSerializer, ReactionSerializer, FeedbackSerializer, ChapterSerializer
from benie_app.models import Story, Tag, Reaction, Feedback, Chapter

# Create your views here.
def home(request):
    stories = Story.objects.all()
    likes = Reaction.objects.all().filter(like=True)
    dislikes = Reaction.objects.all().filter(like=False)
    return render(request,'index.html',{"stories":stories,"likes":likes,"dislikes":dislikes,})

class AllStories(APIView):
    def get(self,request):
        stories = Story.objects.all()
        serializers = StorySerializer(stories,many=True)
        return Response(serializers.data)

class AllTags(APIView):
    def get(self,request):
        tags = Tag.objects.all()
        serializers = TagSerializer(tags,many=True)
        return Response(serializers.data)

class AllFeedbacks(APIView):
    def get(self,request):
        feedbacks = Feedback.objects.all()
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)

class AllRecations(APIView):
    def get(self,request):
        reactions = Reaction.objects.all()
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

class AllChapters(APIView):
    def get(self,request):
        chapters = Chapter.objects.all()
        serializers = ChapterSerializer(chapters,many=True)
        return Response(serializers.data)