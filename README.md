# RPA Lab Assignment

First of all, thank you so much for this wonderful opportunity. I have used django framework to complete the given task. Beside using django framework, I have used moviepy
to get size of the video.

## Dependencies
1. Django Framework
2. Django REST Framework
3. Moviepy Framework

## Directory Structure
API Module : It consists of serializers and views to handle the request.
Video Module : It consists of models.py file to store the video information to the database. It consists of (caption, video, duration, size)

## Implementation

### Adding Video

url : /add/, method : POST, fields : caption, video file

Let's talk about validation at first. Extension of video is validated by first getting extension from the filename of the video and comparing it to list of valid
extensions.

Main challenge lies in validation of size and duration as it is not readily available. So, for this video is uploaded to app. Once it is uploaded, size is calculated
by using os.path.getsize() method. Duration of video is given by VideoFileClip object from movie.py. Since file has to be uploaded for validation, it must be deleted
if validation fails. Another challenge arose when immediately deleting the video file. So, I have created helper function 'clean_up' to delete files that are in directory
but not in database.

Updating to database is self explanatory as serializer class handles it. After validation is successfull, duration and size is updated to database.


### List of videos and filter

url : /all/, method : GET, fields : min_duration (optional), max_duration (optional)

Filtering is optional. If min_duration and max_duration is provided as parameters, filtering is done by using built in function, 'param__lte' and 'param__gte' of django.
If filtering parameter is not provided, all records are returned.

### Calculating charge

url : /charge/, method : POST, fields : size, duration

Once the data is available from the post method, charge is calculated simply using if else statement. This method was first designed to receive video file but later on
modified to get user input.


