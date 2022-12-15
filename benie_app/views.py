from django.shortcuts import render
from benie_app.models import Story, Reaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAdminUser

from benie_app.serializers import StorySerializer, TagSerializer, ReactionSerializer, FeedbackSerializer, ChapterSerializer
from benie_app.models import Story, Tag, Reaction, Feedback, Chapter

# Create your views here.
def landing(request):
    return render(request,'landing.html',{})
    
def home(request):
    stories = Story.objects.all()
    chapters = Chapter.objects.all()
    return render(request,'index.html',{"stories":stories,"chapters":chapters})

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

    def post(self, request):
        serializers = FeedbackSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class AllRecations(APIView):
    def get(self,request):
        reactions = Reaction.objects.all()
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = ReactionSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

class AllChapters(APIView):
    def get(self,request):
        chapters = Chapter.objects.all()
        serializers = ChapterSerializer(chapters,many=True)
        return Response(serializers.data)

class StoryDetails(APIView):
    def get(self,request, id):
        story = Story.objects.all().filter(pk=id).last()
        serializers = StorySerializer(story,many=False)
        return Response(serializers.data)

class ChapterDetails(APIView):
    def get(self,request, id):
        chapter = Chapter.objects.all().filter(pk=id).last()
        serializers = ChapterSerializer(chapter,many=False)
        return Response(serializers.data)

class Likes(APIView):
    def get(self, request, id):
        likes = Reaction.objects.all().filter(chapter=id)
        chap_likes = likes.count 
        serializers = ReactionSerializer(chap_likes,many=True)
        return Response(serializers.data)

class Comments(APIView):
    def get(self, request, id):
        comments = Feedback.objects.all().filter(chapter=id)
        chap_comments = comments.count 
        serializers = FeedbackSerializer(chap_comments,many=True)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class AddStory(APIView):
    def post(self, request):
        serializers = StorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

@permission_classes([IsAdminUser,])
class UpdateStory(APIView):
    def put(self, request, id, format=None):
        story = Story.objects.all().filter(pk=id).last()
        serializers = StorySerializer(story,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        story = Story.objects.all().filter(pk=id).last()
        story.delete()
        return Response(status=status.HTTP_200_OK) 
