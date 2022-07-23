from requests import delete
from rest_framework.response import Response
from rest_framework.decorators import api_view
from video.models import Video
from .serializers import ItemSerializer, VideoSerializer
from moviepy.editor import VideoFileClip
from django.conf import settings
from django.conf.urls.static import static
import os

@api_view(['GET'])
def getData(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)

    return Response(serializer.data)

accepted_extension = ["mp4", "mkv"]

@api_view(['POST'])
def addItem(request):

    # Deleting previous unwanted data
    clean_up()

    # Checking video extension type
    if request.FILES["video"].name.split('.')[1] not in accepted_extension:
        return Response("Video extension must be mp4 or mkv")

    # Saving object
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    main_file = str(settings.BASE_DIR) + serializer.data["video"]

    # Calculating size of video
    if os.path.getsize(main_file)/(1024*1024*1024) >= 1.0:
        deleteObj(serializer)
        return Response("Video Size is more than 1 GB")

    # Calculating length of video
    video_clip = VideoFileClip(main_file)
    if video_clip.duration >= 600:
        deleteObj(serializer)
        return Response("Video length is more than 10 minute")

    return Response("Data successfully updated")


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
