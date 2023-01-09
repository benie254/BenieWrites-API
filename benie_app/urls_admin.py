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
    url(r'^contacts/all/$',views.Contacts.as_view(),name='contacts'),
    url(r'^contact/details/(\d+)$',views.ContactDetails.as_view(),name='contact-details'),
    url(r'^notification/details/(\d+)$',views.NotificationDetails.as_view(),name='notification-details'),
    path('subscriber/details/<str:id>',views.SubscriberDetails.as_view(),name='subscriber-details'),
    url(r'^pages/all/$',views.AllPages.as_view(),name='all-pages'),
    url(r'^story/add/$',views.AddStory.as_view(),name='add-story'),
    url(r'^tag/add/$',views.AddTag.as_view(),name='add-tag'),
    url(r'^chapter/add/$',views.AddChapter.as_view(),name='add-chapter'),
    url(r'^page/add/$',views.AddPage.as_view(),name='add-page'),
    url(r'^story/update/(\d+)$',views.UpdateStory.as_view(),name='update-story'),
    url(r'^chapter/update/(\d+)$',views.UpdateChapter.as_view(),name='update-chapter'),
    url(r'^page/update/(\d+)$',views.UpdatePage.as_view(),name='update-page'),
    url(r'^tag/details/(\d+)$',views.TagDetails.as_view(),name='tag-details'),
    url(r'^page/details/(\d+)$',views.PageDetails.as_view(),name='page-details'),
    url(r'^feedback/details/(\d+)$',views.FeedbackDetails.as_view(),name='feedback-details'),
    url(r'^reaction/details/(\d+)$',views.ReactionDetails.as_view(),name='reaction-details'),
    url(r'^poems/add/$',views.AddPoem.as_view(),name='add-poem'),
    url(r'^poem/update/(\d+)$',views.UpdatePoem.as_view(),name='update-poem'),
]