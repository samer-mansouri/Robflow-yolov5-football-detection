from django.db import models

class VideoUpload(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title
    
class DetectionResults(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    result_video_path = models.CharField(max_length=100)

    def __str__(self):
        return self.video.title