from django.shortcuts import render
from .models import Video

# Create your views here.
def index(request):
    videos = Video.objects.all()
    context = { "videos":videos }

    return render(request, "index.html", context)