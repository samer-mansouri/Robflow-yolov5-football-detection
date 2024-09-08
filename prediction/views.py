from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VideoUploadForm
# from .models import VideoUpload  # Assuming you have a Video model to save the file
from .utils import extract_frames, run_detection_on_images, make_result_video  # Import the extract_frames function
from .models import DetectionResults, VideoUpload
from django.views.generic import ListView

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()  # Save the uploaded video
            video_path = video.video.path  # Get the file path of the saved video
            video_id = video.id  # Get the ID of the saved video
            interval = 5  # Interval in seconds

            try:
                # Call the extract_frames function to extract frames from the uploaded video
                extract_frames(video_path, video_id, interval)
                run_detection_on_images(video_id)
                video_result_path = make_result_video(video_id)
                detection_result = DetectionResults(video=video, result_video_path=video_result_path)
                detection_result.save()
                return JsonResponse({'message': 'Video uploaded and frames extracted successfully!', 
                                        'result_video_path': video_result_path
                                     }, status=200)
            except Exception as e:
                return JsonResponse({'message': f'Error during frame extraction: {str(e)}'}, status=500)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = VideoUploadForm()
    
    return render(request, 'prediction/upload_video.html', {'form': form})

class PredictionResultsView(ListView):
    model = DetectionResults
    template_name = 'prediction_results.html'
    context_object_name = 'detection_results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related video uploads to context
        context['video_uploads'] = VideoUpload.objects.all()
        return context
