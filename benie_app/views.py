from django.shortcuts import render
from benie_app.models import Story, Reaction

# Create your views here.
def home(request):
    stories = Story.objects.all()
    likes = Reaction.objects.all().filter(like=True)
    dislikes = Reaction.objects.all().filter(like=False)
    return render(request,'index.html',{"stories":stories,"likes":likes,"dislikes":dislikes,})
