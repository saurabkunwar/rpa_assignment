from rest_framework.response import Response
from rest_framework.decorators import api_view
from video.models import Video
from .serializers import VideoSerializer
from moviepy.editor import VideoFileClip
from django.conf import settings
import os

@api_view(['GET'])
def getData(request):

    # Filtering based on duration
    if "min_duration" in request.GET and "max_duration" in request.GET:
        videos = Video.objects.filter(duration__gte=request.GET["min_duration"], duration__lte=request.GET["max_duration"])
    else:
        videos = Video.objects.all()

    serializer = VideoSerializer(videos, many=True)

    return Response(serializer.data)

accepted_extension = ["mp4", "mkv"]

@api_view(['POST'])
def addItem(request):

    # Checking video extension type
    if request.FILES["video"].name.split('.')[1] not in accepted_extension:
        return Response({"message": "Video extension must be mp4 or mkv"})

    # Saving object
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    main_file = str(settings.BASE_DIR) + serializer.data["video"]

    # Calculating size and duration of video
    size = os.path.getsize(main_file)/(1024*1024)
    video_clip = VideoFileClip(main_file)
    duration = video_clip.duration

    # Validating size
    if size > 1024:
        deleteObj(serializer)
        return Response({"message": "Video Size is more than 1 GB"})

    # Validating length of video
    if duration >= 600:
        deleteObj(serializer)
        return Response({"message": "Video length is more than 10 minute"})

    # Update duration and size in database
    video_obj  = Video.objects.get(pk=serializer.data["id"])
    video_obj.size = size
    video_obj.duration = duration
    video_obj.save()

    # Deleting previous unwanted data
    clean_up()

    return Response({"message": "Data successfully updated"})

@api_view(['POST'])
def charge(request):

    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    main_file = str(settings.BASE_DIR) + serializer.data["video"]

    # Calculating size of video
    size = os.path.getsize(main_file)/(1024*1024)

    # Calculating length of video
    video_clip = VideoFileClip(main_file)
    duration = video_clip.duration

    # Calculating charges
    charge = 0
    charge += 6 if size<500 else 12.5
    charge += 12.5 if duration<378 else 20

    deleteObj(serializer)

    return Response({'charge': charge})


def deleteObj(serializer):
    # Delete unsuccessfull object
    id = int(serializer.data["id"])
    video_obj = Video.objects.get(pk=id)
    video_obj.delete()

# This method removes uploaded videos
def clean_up():
    file_videos = os.listdir(settings.MEDIA_ROOT+r"\video")
    database_url = list(Video.objects.all().values_list('video'))

    db_videos = []

    # Clean database videos
    for db_video in database_url:
        db_videos.append(db_video[0].split('/')[1])

    # Check if videos on directory exists in database, if not, delete the video
    for f_video in file_videos:
        if f_video not in db_videos:
            video_file = rf"\video\{f_video}"
            os.remove(settings.MEDIA_ROOT+video_file)
