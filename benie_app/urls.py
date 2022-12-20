"""benie_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path as url
from benie_app import views 

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^stories/all/$',views.AllStories.as_view(),name='all-stories'),
    url(r'^stories/ongoing/$',views.OngoingStories.as_view(),name='ongoing-stories'),
    url(r'^stories/completed/$',views.CompletedStories.as_view(),name='completed-stories'),
    url(r'^story/details/(\d+)$',views.StoryDetails.as_view(),name='story-details'),
    url(r'^story/chapters/(\d+)$',views.StoryChapters.as_view(),name='story-chapters'),
    url(r'^tags/all/$',views.AllTags.as_view(),name='all-tags'),
    url(r'^feedbacks/all/$',views.AllFeedbacks.as_view(),name='all-feedbacks'),
    url(r'^story/feedbacks/(\d+)$',views.StoryFeedbacks.as_view(),name='story-feedbacks'),
    url(r'^reactions/all/$',views.AllRecations.as_view(),name='all-reactions'),
    url(r'^notifications/all/$',views.Notifications.as_view(),name='notifications'),
    url(r'^story/reactions/(\d+)$',views.StoryReactions.as_view(),name='story-reactions'),
    url(r'^chapters/all/$',views.AllChapters.as_view(),name='all-chapters'),
    url(r'^chapter/details/(\d+)$',views.ChapterDetails.as_view(),name='chapter-details'),
    url(r'^chapter/pages/(\d+)$',views.ChapterPages.as_view(),name='chapter-pages'),
    url(r'^chapter/details/(\d+)$',views.PageDetails.as_view(),name='chapter-details'),
    url(r'^newsletter/subscribers/$',views.AllSubscribers.as_view(),name='newsletter-subscribers'),
    #admin
    url(r'^admin/notification/details/(\d+)$',views.NotificationDetails.as_view(),name='notification-details'),
    url(r'^admin/subscriber/details/(\d+)$',views.SubscriberDetails.as_view(),name='subscriber-details'),
    url(r'^admin/pages/all/$',views.AllPages.as_view(),name='all-pages'),
    url(r'^admin/story/add/$',views.AddStory.as_view(),name='add-story'),
    url(r'^admin/tag/add/$',views.AddTag.as_view(),name='add-tag'),
    url(r'^admin/chapter/add/$',views.AddChapter.as_view(),name='add-chapter'),
    url(r'^admin/page/add/$',views.AddPage.as_view(),name='add-page'),
    url(r'^admin/story/update/(\d+)$',views.UpdateStory.as_view(),name='update-story'),
    url(r'^admin/chapter/update/(\d+)$',views.UpdateChapter.as_view(),name='update-chapter'),
    url(r'^admin/page/update/(\d+)$',views.UpdatePage.as_view(),name='update-page'),
    url(r'^admin/tag/details/(\d+)$',views.TagDetails.as_view(),name='tag-details'),
    url(r'^admin/page/details/(\d+)$',views.PageDetails.as_view(),name='page-details'),
    url(r'^admin/feedback/details/(\d+)$',views.FeedbackDetails.as_view(),name='feedback-details'),
    url(r'^admin/reaction/details/(\d+)$',views.ReactionDetails.as_view(),name='reaction-details'),
]
