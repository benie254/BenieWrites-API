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
    url(r'^story/details/(\d+)$',views.StoryDetails.as_view(),name='story-details'),
    url(r'^tags/all/$',views.AllTags.as_view(),name='all-tags'),
    url(r'^feedbacks/all/$',views.AllFeedbacks.as_view(),name='all-feedbacks'),
    url(r'^reactions/all/$',views.AllRecations.as_view(),name='all-reactions'),
    url(r'^chapters/all/$',views.AllChapters.as_view(),name='all-chapters'),
    url(r'^chapter/details/(\d+)$',views.ChapterDetails.as_view(),name='chapter-details'),
    #admin
    url(r'^admin/story/add/$',views.AddStory.as_view(),name='add-story'),
    url(r'^admin/story/edit/(\d+)$',views.UpdateStory.as_view(),name='edit-story'),
    url(r'^admin/story/delete/(\d+)$',views.UpdateStory.as_view(),name='delete-story'),
]