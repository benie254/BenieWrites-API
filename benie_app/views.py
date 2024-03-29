from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Sum
from django.http import Http404 

import datetime as dt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError

import sendgrid
from sendgrid.helpers.mail import * 
from decouple import config 

from benie_app.serializers import StorySerializer, TagSerializer, ReactionSerializer, FeedbackSerializer, DelSubSerializer, ReplySerializer, ChapterSerializer, PageSerializer, SubscriberSerializer, NotificationSerializer, ContactSerializer, PoemSerializer
from benie_app.models import Story, Tag, Reaction, Feedback, Chapter, Page, Subscriber, Notification, Contact, Poem, Reply



# Create your views here.
@permission_classes([IsAuthenticatedOrReadOnly,])
def landing(request):
    return render(request,'landing.html',{})
    
@permission_classes([IsAuthenticatedOrReadOnly,])
def home(request):
    stories = Story.objects.all()
    chapters = Chapter.objects.all()
    return render(request,'index.html',{"stories":stories,"chapters":chapters})

@permission_classes([IsAuthenticatedOrReadOnly,])
class AllStories(APIView):
    def get(self,request):
        stories = Story.objects.all().order_by('-first_published')
        serializers = StorySerializer(stories,many=True)
        story = Story.objects.filter(pin='pinned').last()
        if story:
            story_id = story.id
            chapters = Chapter.objects.filter(story=story_id)
            reactions = Reaction.objects.filter(story=story_id)
            feedbacks = Feedback.objects.filter(story=story_id)
            story.words = chapters.aggregate(TOTAL=Sum('words'))['TOTAL']
            story.save()
            story.refresh_from_db()
            if chapters:
                story.chaps = chapters.count()
                story.save()
                story.refresh_from_db()
            if reactions:
                story.likes = reactions.count()
                story.save()
                story.refresh_from_db()
            if feedbacks:
                story.comments = feedbacks.count()
                story.save()
                story.refresh_from_db()
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class OngoingStories(APIView):
    def get(self,request):
        stories = Story.objects.all().filter(status='ongoing').order_by('-first_published')
        if stories:
            serializers = StorySerializer(stories,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticatedOrReadOnly,])
class CompletedStories(APIView):
    def get(self,request):
        stories = Story.objects.all().filter(status='completed').order_by('-first_published')
        if stories:
            serializers = StorySerializer(stories,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticatedOrReadOnly,])
class AllTags(APIView):
    def get(self,request):
        tags = Tag.objects.all()
        serializers = TagSerializer(tags,many=True)
        return Response(serializers.data)

@permission_classes([AllowAny,])
class AllFeedbacks(APIView):
    def get(self,request):
        feedbacks = Feedback.objects.all().order_by('-date')
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)
    def post(self, request):
        serializers = FeedbackSerializer(data=request.data)
        if serializers.is_valid():
            comment = serializers.validated_data['comment']
            commented_by = serializers.validated_data['commented_by']
            st = serializers.validated_data['story']
            pm = serializers.validated_data['poem']
            if st:
                story = Story.objects.filter(title=st).last()
                stp = 'Story commented'
            else:
                story = '0'
                stp = 'Not a story'
            if pm:
                poem = Poem.objects.filter(title=pm).last()
                pmp = 'Poem commented'
            else:
                poem = '0'
                pmp = 'Not a poem'
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/new-comment.html', {
                'story':story,
                'stp': stp,
                'poem': poem,
                'pmp': pmp,
                'poem_id': st,
                'comment': comment,
                'commented_by': commented_by,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'beniewrites@gmail.com',
                subject = "New Comment",
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
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny,])
class AllReplies(APIView):
    def get(self,request):
        replies = Reply.objects.all().order_by('-date')
        serializers = ReplySerializer(replies,many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = ReplySerializer(data=request.data)
        if serializers.is_valid():
            cmnt = serializers.validated_data['comment']
            replied_by = serializers.validated_data['replied_by']
            content = serializers.validated_data['msg']
            reply = Reply.objects.filter(comment=cmnt).last()
            st = serializers.validated_data['story']
            pm = serializers.validated_data['poem']
            if st:
                story = Story.objects.filter(title=st).last()
                stp = 'Story commented'
            else:
                story = '0'
                stp = 'Not a story'
            if pm:
                poem = Poem.objects.filter(title=pm).last()
                pmp = 'Poem commented'
            else:
                poem = '0'
                pmp = 'Not a poem'
            serializers.save()
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/new-reply.html', {
                'replied_by':replied_by,
                'content': content,
                'reply': reply,
                'stp': stp,
                'pmp': pmp,
                'poem': poem,
                'story':story,
                'comment': cmnt,
            })
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = 'beniewrites@gmail.com',
                subject = "New Reply",
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
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                }
            Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny,])
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

@permission_classes([IsAuthenticatedOrReadOnly,])
class AllChapters(APIView):
    def get(self,request):
        chapters = Chapter.objects.all()
        serializers = ChapterSerializer(chapters,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class AllPages(APIView):
    def get(self,request):
        pages = Page.objects.all()
        serializers = PageSerializer(pages,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class AllPoems(APIView):
    def get(self,request):
        poems = Poem.objects.all().order_by('-uploaded')
        serializers = PoemSerializer(poems,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class PinnedPoem(APIView):
    def get(self,request):
        poems = Poem.objects.all().filter(status='pinned').last()
        serializers = PoemSerializer(poems,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class RelatedPoems(APIView):
    def get(self,request, category):
        poems = Poem.objects.all().filter(category=category).order_by('title')
        serializers = PoemSerializer(poems,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class RelatedStories(APIView):
    def get(self,request, id):
        by_categ = Story.objects.all().filter(category=id).order_by('title')
        by_genre = Story.objects.all().filter(genre=id).order_by('title')
        by_status = Story.objects.all().filter(status=id).order_by('title')
        if by_categ:
            serializers = StorySerializer(by_categ,many=True)
            return Response(serializers.data)
        if by_genre:
            serializers = StorySerializer(by_genre,many=True)
            return Response(serializers.data)
        if by_status:
            serializers = StorySerializer(by_status,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticatedOrReadOnly,])
class StoryDetails(APIView):
    def get(self,request, id):
        story = Story.objects.all().filter(pk=id).last()
        serializers = StorySerializer(story,many=False)
        chapters = Chapter.objects.all().filter(story=id).order_by('pk')
        reactions = Reaction.objects.all().filter(story=id).order_by('pk')
        feedbacks = Feedback.objects.all().filter(story=id).order_by('pk')
        if story:
            story.words = chapters.aggregate(TOTAL=Sum('words'))['TOTAL']
            story.save()
            story.refresh_from_db()
        if chapters:
            story.chaps = chapters.count()
            story.save()
            story.refresh_from_db()
        if reactions:
            story.likes = reactions.count()
            story.save()
            story.refresh_from_db()
        if feedbacks:
            story.comments = feedbacks.count()
            story.save()
            story.refresh_from_db()
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class PageDetails(APIView):
    def get(self,request, id):
        page = Page.objects.all().filter(pk=id).last()
        serializers = PageSerializer(page,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class ChapterDetails(APIView):
    def get(self,request, id):
        chapter = Chapter.objects.all().filter(pk=id).last()
        serializers = ChapterSerializer(chapter,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class PoemDetails(APIView):
    def get(self,request, id):
        poem = Poem.objects.all().filter(pk=id).last()
        serializers = PoemSerializer(poem,many=False)
        return Response(serializers.data)

@permission_classes([AllowAny,])
class ChapterReactions(APIView):
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

    
@permission_classes([IsAuthenticatedOrReadOnly,])
class Feedbacks(APIView):
    def get(self, request, id):
        comments = Feedback.objects.all().filter(chapter=id)
        serializers = FeedbackSerializer(comments,many=True)
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
class AddPoem(APIView):
    def post(self, request):
        serializers = PoemSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

@permission_classes([IsAdminUser,])
class AddPage(APIView):
    def post(self, request):
        serializers = PageSerializer(data=request.data)
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
class AddChapter(APIView):
    def post(self, request):
        serializers = ChapterSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

@permission_classes([IsAdminUser,])
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
        
@permission_classes([IsAdminUser,])
class AddTag(APIView):
    def post(self, request):
        serializers = TagSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 



@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
class ReactionDetails(APIView):
    def get(self,request, id):
        reaction = Reaction.objects.all().filter(pk=id).last()
        serializers = ReactionSerializer(reaction,many=False)
        return Response(serializers.data)

    def delete(self, request, id, format=None):
        reaction = Reaction.objects.all().filter(pk=id).last()
        reaction.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAdminUser,])
class FeedbackDetails(APIView):
    def get(self,request, id):
        comment = Feedback.objects.all().filter(pk=id).last()
        likes = Reaction.objects.all().filter(comment=id).order_by('-date')
        replies = Reply.objects.all().filter(comment=id).order_by('-date')
        if replies:
            comment.replies = replies.count() 
            comment.save()
            comment.refresh_from_db
        if likes:
            comment.likes = likes.count() 
            comment.save()
            comment.refresh_from_db
        print("replies",comment.replies)
        serializers = FeedbackSerializer(comment,many=False)
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

@permission_classes([IsAuthenticatedOrReadOnly,])
class StoryChapters(APIView):
    def get(self,request, id):
        chapters = Chapter.objects.all().filter(story=id).order_by('pk')
        story = Story.objects.all().filter(pk=id).last()
        if story:
            story.words = chapters.aggregate(TOTAL=Sum('words'))['TOTAL']
            story.save()
            story.refresh_from_db()
        if chapters:
            story.chaps = chapters.count()
            story.save()
            story.refresh_from_db()
        serializers = ChapterSerializer(chapters,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class StoryReactions(APIView):
    def get(self, request, id):
        reactions = Reaction.objects.all().filter(story=id).filter(like='like')
        story = Story.objects.all().filter(pk=id).last()
        if reactions:
            story.likes = reactions.count()
            story.save()
            story.refresh_from_db()
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class StoryFeedbacks(APIView):
    def get(self, request, id):
        feedbacks = Feedback.objects.all().filter(story=id).order_by('-date')
        story = Story.objects.all().filter(pk=id).last()
        if feedbacks:
            story.comments = feedbacks.count()
            story.save()
            story.refresh_from_db()
        
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class PoemReactions(APIView):
    def get(self, request, id):
        reactions = Reaction.objects.all().filter(poem=id).filter(like='like')
        serializers = ReactionSerializer(reactions,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class PoemFeedbacks(APIView):
    def get(self, request, id):
        feedbacks = Feedback.objects.all().filter(poem=id).order_by('-date')
        serializers = FeedbackSerializer(feedbacks,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class FeedbackReplies(APIView):
    def get(self, request, id):
        replies = Reply.objects.all().filter(comment=id).order_by('-date')
        comment = Feedback.objects.all().filter(pk=id).last()
        comment.replies = replies.count() 
        comment.save()
        comment.refresh_from_db
        serializers = ReplySerializer(replies,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticatedOrReadOnly,])
class FeedbackLikes(APIView):
    def get(self, request, id):
        likes = Reaction.objects.all().filter(comment=id).order_by('-date')
        comment = Feedback.objects.all().filter(pk=id).last()
        if comment:
            comment.likes = likes.count() 
            comment.save()
            comment.refresh_from_db
            serializers = ReplySerializer(likes,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticatedOrReadOnly,])
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

@permission_classes([AllowAny,])
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

@permission_classes([AllowAny,])
class Unsubscribe(APIView):
    def get(self,request,user_email):
        subscriber = Subscriber.objects.all().filter(email=user_email).last()
        serializers = SubscriberSerializer(subscriber,many=False)
        return Response(serializers.data)

    def delete(self, request, user_email, format=None):
        subscriber = Subscriber.objects.all().filter(email=user_email).last()
        if subscriber:
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = render_to_string('email/unsubscribed.html', {
                    'email': user_email,
            })
            message = Mail(
                    from_email = Email("davinci.monalissa@gmail.com"),
                    to_emails = 'beniewrites@gmail.com',
                    subject = "Subscriber Optout",
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
            msg2 = render_to_string('email/goodbye-subscriber.html', {
                    'email': user_email,
                })
            message2 = Mail(
                    from_email = Email("davinci.monalissa@gmail.com"),
                    to_emails = user_email,
                    subject = "Unsubscribed",
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
            response = {
                    'success' : 'True',
                    }
            subscriber.delete()
            return Response(status=status.HTTP_200_OK) 
        return Response(status=status.HTTP_421_MISDIRECTED_REQUEST)
        
            
@permission_classes([AllowAny,])
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAdminUser,])
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

@permission_classes([IsAuthenticatedOrReadOnly,])
class PastPoems(APIView):
    def get(self,request,date):
        poems = Poem.search(date)
        if poems:
            serializers = PoemSerializer(poems,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
