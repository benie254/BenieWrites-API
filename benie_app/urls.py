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
    url(r'^replies/all/$',views.AllReplies.as_view(),name='all-replies'),
    url(r'^story/feedbacks/(\d+)$',views.StoryFeedbacks.as_view(),name='story-feedbacks'),
    url(r'^reactions/all/$',views.AllRecations.as_view(),name='all-reactions'),
    url(r'^notifications/all/$',views.Notifications.as_view(),name='notifications'),
    url(r'^story/reactions/(\d+)$',views.StoryReactions.as_view(),name='story-reactions'),
    path('stories/related/<id>',views.RelatedStories.as_view(),name='related-stories'),
    url(r'^chapters/all/$',views.AllChapters.as_view(),name='all-chapters'),
    url(r'^chapter/details/(\d+)$',views.ChapterDetails.as_view(),name='chapter-details'),
    url(r'^chapter/pages/(\d+)$',views.ChapterPages.as_view(),name='chapter-pages'),
    url(r'^chapter/details/(\d+)$',views.PageDetails.as_view(),name='chapter-details'),
    url(r'^newsletter/subscribers/$',views.AllSubscribers.as_view(),name='newsletter-subscribers'),
    url(r'^poems/all/$',views.AllPoems.as_view(),name='all-poems'),
    path('poems/related/<str:category>',views.RelatedPoems.as_view(),name='related-poems'),
    url(r'^poem/details/(\d+)$',views.PoemDetails.as_view(),name='poem-details'),
    url(r'^poem/pinned/$',views.PinnedPoem.as_view(),name='pinned-poem'),
    url(r'^poem/reactions/(\d+)$',views.PoemReactions.as_view(),name='poem-reactions'),
    url(r'^poem/feedbacks/(\d+)$',views.PoemFeedbacks.as_view(),name='poem-feedbacks'),
    url(r'^feedback/replies/(\d+)$',views.FeedbackReplies.as_view(),name='poem-feedback-replies'),
    url(r'^feedback/likes/(\d+)$',views.FeedbackLikes.as_view(),name='poem-feedback-likes'),
    url(r'^poems/past/(\d{4}-\d{2}-\d{2})$',views.PastPoems.as_view(),name='past-poems'),
    url(r'^newsletter/unsubscribe/(\d+)',views.Unsubscribe.as_view(),name='unsubscribe'),
]
