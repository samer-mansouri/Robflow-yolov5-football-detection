# utils.py
import cv2
import os
import logging
import subprocess
from moviepy.editor import ImageSequenceClip

def setup_logging():
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("frame_extraction.log"),
            logging.StreamHandler()
        ]
    )

def extract_frames(video_path, video_id, interval):
    setup_logging() 

    # Create a unique folder for each video using the video ID
    output_dir = os.path.join('./output_frames', f'video_{video_id}')
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        logging.error("Error: Could not open video.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval)

    frame_count = 0
    extracted_frame_count = 0

    logging.info(f"Video opened: {video_path}")
    logging.info(f"Video FPS: {fps}")
    logging.info(f"Total frames: {total_frames}")
    logging.info(f"Frame interval (in frames): {frame_interval}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{extracted_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            logging.info(f"Extracted frame {extracted_frame_count}: {frame_filename}")
            extracted_frame_count += 1

        frame_count += 1
        if frame_count % (frame_interval * 10) == 0:
            logging.info(f"Processed {frame_count} frames out of {total_frames}")

    cap.release()
    logging.info(f"Extraction complete. Extracted {extracted_frame_count} frames.")

def run_detection_on_images(video_id):
    try:
        output_dir = './output_frames'
        results_dir = './results'
        os.makedirs(results_dir, exist_ok=True)

        detect_script = './yolov5/detect.py'
        weights = './yolov5/runs/train/exp6/weights/best.pt'
        img_size = 640
        conf = 0.8

        frames_dir = f'{output_dir}/video_{video_id}'
        results_dir = f'{results_dir}/video_{video_id}'
        os.makedirs(results_dir, exist_ok=True)

        for frame in os.listdir(frames_dir):
            frame_path = os.path.join(frames_dir, frame)

            command = [
                'python', detect_script,
                '--weights', weights,
                '--img', str(img_size),
                '--conf', str(conf),
                '--source', frame_path,
                '--project', results_dir,    # Desired results directory
                # '--name', 'detected_images'  # Subfolder inside results directory
            ]

            print(f'Running command: {" ".join(command)}')

            try:
                result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print('Detection result:')
                print(result.stdout.decode())
            except subprocess.CalledProcessError as e:
                print(f'Error running command: {e}')
                print('Standard output:')
                print(e.stdout.decode())
                print('Standard error:')
                print(e.stderr.decode())

    except Exception as e:
        print(f'Error during frame detection: {str(e)}')


def make_result_video(video_id):

    try:
        frames_dir = f'./results/video_{video_id}'

        print(f'Creating video from frames in {frames_dir}')

        ##if ouput_videos directory does not exist, create it
        if not os.path.exists('./output_videos'):
            os.makedirs('./output_videos')


        output_video_path = f'./output_videos/video_{video_id}.mp4'

        ## the structure is like this for example: ./results/video_1/exp/frame_55 and inside video_1 there are many exp folders exp, exp2, exp3, etc
        imgs_paths = []
        for root, dirs, files in os.walk(frames_dir):
            for file in files:
                if file.endswith('.jpg'):
                    imgs_paths.append(os.path.join(root, file))

        imgs_paths.sort()

        # Create a video clip from the sequence of images
        clip = ImageSequenceClip(imgs_paths, fps=5)

        # Write the video file
        clip.write_videofile(output_video_path, codec='libx264', fps=5)

        print(f'Video created: {output_video_path}')

        return f'/output_videos/video_{video_id}.mp4'


    
    except Exception as e:
        print(f'Error during video creation: {str(e)}')
        return None




