from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Sum
from django.http import Http404 

import datetime as dt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAdminUser

import sendgrid
from sendgrid.helpers.mail import * 
from decouple import config 

from benie_app.serializers import StorySerializer, TagSerializer, ReactionSerializer, FeedbackSerializer, ChapterSerializer, PageSerializer, SubscriberSerializer, NotificationSerializer, ContactSerializer, PoemSerializer
from benie_app.models import Story, Tag, Reaction, Feedback, Chapter, Page, Subscriber, Notification, Contact, Poem

# Create your views here.
def landing(request):
    return render(request,'landing.html',{})
    
def home(request):
    stories = Story.objects.all()
    chapters = Chapter.objects.all()
    return render(request,'index.html',{"stories":stories,"chapters":chapters})

class AllStories(APIView):
    def get(self,request):
        stories = Story.objects.all().order_by('-first_published')
        serializers = StorySerializer(stories,many=True)
        return Response(serializers.data)

class OngoingStories(APIView):
    def get(self,request):
        stories = Story.objects.all().filter(status='ongoing').order_by('-first_published')
        serializers = StorySerializer(stories,many=True)
        return Response(serializers.data)

class CompletedStories(APIView):
    def get(self,request):
        stories = Story.objects.all().filter(status='completed').order_by('-first_published')
        serializers = StorySerializer(stories,many=True)
        return Response(serializers.data)

class AllTags(APIView):
    def get(self,request):
        tags = Tag.objects.all()
        serializers = TagSerializer(tags,many=True)
        return Response(serializers.data)

class AllFeedbacks(APIView):
    def get(self,request):
        feedbacks = Feedback.objects.all().order_by('-date')
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

class AllPages(APIView):
    def get(self,request):
        pages = Page.objects.all()
        serializers = PageSerializer(pages,many=True)
        return Response(serializers.data)

class AllPoems(APIView):
    def get(self,request):
        poems = Poem.objects.all().order_by('-uploaded')
        serializers = PoemSerializer(poems,many=True)
        return Response(serializers.data)

class PinnedPoem(APIView):
    def get(self,request):
        poems = Poem.objects.all().filter(status='pinned').last()
        serializers = PoemSerializer(poems,many=False)
        return Response(serializers.data)

class RelatedPoems(APIView):
    def get(self,request, category):
        poems = Poem.objects.all().filter(category=category).order_by('title')
        serializers = PoemSerializer(poems,many=True)
        return Response(serializers.data)

class StoryDetails(APIView):
    def get(self,request, id):
        story = Story.objects.all().filter(pk=id).last()
        serializers = StorySerializer(story,many=False)
        return Response(serializers.data)

class PageDetails(APIView):
    def get(self,request, id):
        page = Page.objects.all().filter(pk=id).last()
        serializers = PageSerializer(page,many=False)
        return Response(serializers.data)

class ChapterDetails(APIView):
    def get(self,request, id):
        chapter = Chapter.objects.all().filter(pk=id).last()
        serializers = ChapterSerializer(chapter,many=False)
        return Response(serializers.data)

class PoemDetails(APIView):
    def get(self,request, id):
        poem = Poem.objects.all().filter(pk=id).last()
        serializers = PoemSerializer(poem,many=False)
        return Response(serializers.data)

class Reactions(APIView):
    def get(self, request, id):
        likes = Reaction.objects.all().filter(chapter=id)
        serializers = ReactionSerializer(likes,many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = ReactionSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    

class Feedbacks(APIView):
    def get(self, request, id):
        comments = Feedback.objects.all().filter(chapter=id)
        serializers = FeedbackSerializer(comments,many=True)
        return Response(serializers.data)

# @permission_classes([IsAdminUser,])
class AddStory(APIView):
    def post(self, request):
        serializers = StorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  


class AddPoem(APIView):
    def post(self, request):
        serializers = PoemSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

# @permission_classes([IsAdminUser,])
class AddPage(APIView):
    def post(self, request):
        serializers = PageSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

# @permission_classes([IsAdminUser,])
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

# @permission_classes([IsAdminUser,])
class UpdatePage(APIView):
    def put(self, request, id, format=None):
        page = Page.objects.all().filter(pk=id).last()
        serializers = PageSerializer(page,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        page = Page.objects.all().filter(pk=id).last()
        page.delete()
        return Response(status=status.HTTP_200_OK) 

class UpdatePoem(APIView):
    def put(self, request, id, format=None):
        poem = Poem.objects.all().filter(pk=id).last()
        serializers = PoemSerializer(poem,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        poem = Poem.objects.all().filter(pk=id).last()
        poem.delete()
        return Response(status=status.HTTP_200_OK) 

# @permission_classes([IsAdminUser,])
class AddChapter(APIView):
    def post(self, request):
        serializers = ChapterSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

# @permission_classes([IsAdminUser,])
class UpdateChapter(APIView):
    def put(self, request, id, format=None):
        chap = Chapter.objects.all().filter(pk=id).last()
        serializers = ChapterSerializer(chap,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        chap = Chapter.objects.all().filter(pk=id).last()
        chap.delete()
        return Response(status=status.HTTP_200_OK) 
        
# @permission_classes([IsAdminUser,])
class AddTag(APIView):
    def post(self, request):
        serializers = TagSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 



# @permission_classes([IsAdminUser,])
class TagDetails(APIView):
    def get(self,request, id):
        tag = Tag.objects.all().filter(pk=id).last()
        serializers = TagSerializer(tag,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        tag = Tag.objects.all().filter(pk=id).last()
        serializers = TagSerializer(tag,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        tag = Tag.objects.all().filter(pk=id).last()
        tag.delete()
        return Response(status=status.HTTP_200_OK) 

# @permission_classes([IsAdminUser,])
class ReactionDetails(APIView):
    def get(self,request, id):
        reaction = Reaction.objects.all().filter(pk=id).last()
        serializers = ReactionSerializer(reaction,many=False)
        return Response(serializers.data)

    def delete(self, request, id, format=None):
        reaction = Reaction.objects.all().filter(pk=id).last()
        reaction.delete()
        return Response(status=status.HTTP_200_OK) 

# @permission_classes([IsAdminUser,])
class FeedbackDetails(APIView):
    def get(self,request, id):
        feedback = Feedback.objects.all().filter(pk=id).last()
        serializers = FeedbackSerializer(feedback,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        feedback = Feedback.objects.all().filter(pk=id).last()
        serializers = FeedbackSerializer(feedback,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        feedback = Feedback.objects.all().filter(pk=id).last()
        feedback.delete()
        return Response(status=status.HTTP_200_OK) 

class StoryChapters(APIView):
    def get(self,request, id):
        chapters = Chapter.objects.all().filter(story=id).order_by('pk')
        story = Story.objects.all().filter(pk=id).last()
        if story:
            story.words = chapters.aggregate(TOTAL=Sum('words'))['TOTAL']
            story.save()
            story.refresh_from_db()
        serializers = ChapterSerializer(chapters,many=True)
        return Response(serializers.data)

class StoryReactions(APIView):
    def get(self, request, id):
        reactions = Reaction.objects.all().filter(story=id).filter(like='like')
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

class StoryFeedbacks(APIView):
    def get(self, request, id):
        feedbacks = Feedback.objects.all().filter(story=id).order_by('-date')
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)

class PoemReactions(APIView):
    def get(self, request, id):
        reactions = Reaction.objects.all().filter(story=id).filter(like='like')
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

class PoemFeedbacks(APIView):
    def get(self, request, id):
        feedbacks = Feedback.objects.all().filter(story=id).order_by('-date')
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)

class ChapterPages(APIView):
    def get(self,request, id):
        pages = Page.objects.all().filter(chapter=id).order_by('pk')
        chap = Chapter.objects.all().filter(pk=id).last()
        if chap:
            chap.words = pages.aggregate(TOTAL=Sum('words'))['TOTAL']
            chap.save()
            chap.refresh_from_db()
        serializers = PageSerializer(pages,many=True)
        return Response(serializers.data)

class AllSubscribers(APIView):
    # permission_classes = (IsAdminUser,IsAuthenticated)
    def get(self,request,format=None):
        subscribers = Subscriber.objects.all().order_by('date_subscribed')
        serializers = SubscriberSerializer(subscribers,many=True)
        return Response(serializers.data)

    # permission_classes = (AllowAny)
    def post(self,request,format=None):
        serializers = SubscriberSerializer(data=request.data)
        if serializers.is_valid():
            name = serializers.validated_data['name']
            email = serializers.validated_data['email']
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/new-subscriber.html', {
                'name': name,
                'email': email,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'beniewrites@gmail.com',
                subject = "New Subscriber",
                html_content= msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)

            msg2 = render_to_string('email/welcome-subscriber.html', {
                'name': name,
                'email': email,
            })
            message2 = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = email,
                subject = "Monthly Newsletter",
                html_content= msg2
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message2)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Notifications(APIView):
    def get(self,request):
        notifications = Notification.objects.all().order_by('-date')
        serializers = NotificationSerializer(notifications,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = NotificationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

class NotificationDetails(APIView):
    def get(self,request,id):
        notification = Notification.objects.all().filter(pk=id).last()
        serializers = NotificationSerializer(notification,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        notification = Notification.objects.all().filter(pk=id).last()
        serializers = NotificationSerializer(notification,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        notification = Notification.objects.all().filter(pk=id).last()
        notification.delete()
        return Response(status=status.HTTP_200_OK) 

class Contacts(APIView):
    def get(self,request):
        contacts = Contact.objects.all().order_by('-date')
        serializers = ContactSerializer(contacts,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ContactSerializer(data=request.data)
        if serializers.is_valid():
            name = serializers.validated_data['name']
            email = serializers.validated_data['email']
            message = serializers.validated_data['message']
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/new-contact.html', {
                'name': name,
                'email': email,
                "message": message,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'beniewrites@gmail.com',
                subject = "New Contact",
                html_content= msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)

            msg2 = render_to_string('email/message-delivered.html', {
                'name': name,
            })
            message2 = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = email,
                subject = "Message Delivered",
                html_content= msg2
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message2)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

class ContactDetails(APIView):
    def get(self,request,id):
        contact = Contact.objects.all().filter(pk=id).last()
        serializers = ContactSerializer(contact,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        serializers = ContactSerializer(contact,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

class SubscriberDetails(APIView):
    def get(self,request,id):
        subscriber = Subscriber.objects.all().filter(pk=id).last()
        serializers = SubscriberSerializer(subscriber,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        subscriber = Subscriber.objects.all().filter(pk=id).last()
        serializers = SubscriberSerializer(subscriber,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        subscriber = Subscriber.objects.all().filter(pk=id).last()
        subscriber.delete()
        return Response(status=status.HTTP_200_OK) 


class PastPoems(APIView):
    def get(self,request,date):
        poems = Poem.search(date)
        if poems:
            serializers = PoemSerializer(poems,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)