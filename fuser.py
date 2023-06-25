#!/usr/bin/env python3
# Code by 1ssb on github

import ffmpeg
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/home/users/u7143478/anaconda3/envs/dinov2/plugins'
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 
import time
import warnings
warnings.filterwarnings("ignore")
import imageio
import torch
from PIL import Image
import torchvision.transforms as T
import hubconf
from sklearn.decomposition import PCA
import numpy as np
from PIL import Image
import glob
from moviepy.editor import ImageSequenceClip, VideoFileClip, clips_array
from tqdm import tqdm
import matplotlib.pyplot as plt

def capture_images(c, s=0.1, t=5, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        cap = imageio.get_reader('<video{}>'.format(c))
    except Exception as e:
        print('Error: Could not open camera {}: {}'.format(c, e))
        return
    print("Enter 'c' if you are ready to record for {} seconds".format(t))
    key = input()
    if key != 'c':
        return
    start_time = time.time()
    for _ in tqdm(range(int(t/s)), desc="Capturing Images"):
        try:
            frame = cap.get_next_data()
            filename = 'I-{:.1f}.jpg'.format(time.time() - start_time)
            imageio.imwrite(os.path.join(folder, filename), frame)
            time.sleep(s)
        except Exception as e:
            print('Error: Could not capture image: {}'.format(e))
            break
def extract_features(image_path, destination_path):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    dinov2_vits14 = hubconf.dinov2_vits14().to(device)
    img = Image.open(image_path)
    transforms = T.Compose([
        T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ])
    img = transforms(img)[:3].unsqueeze(0).to(device)
    with torch.no_grad():
        features = dinov2_vits14(img, return_patches=True)[0]
    pca = PCA(n_components=3)
    pca.fit(features.cpu())
    pca_features = pca.transform(features.cpu())
    pca_features = (pca_features - pca_features.min()) / (pca_features.max() - pca_features.min())
    pca_features = pca_features * 255
    plt.imshow(pca_features.reshape(16, 16, 3).astype(np.uint8))
    if not destination_path.endswith('_feature.jpg'):
        destination_path = destination_path.replace('.jpg', '_feature.jpg')
    plt.axis('off')
    plt.savefig(destination_path, bbox_inches='tight', pad_inches=0)
def images_to_video(input_folder, output_path='feature_film.mp4', sampling_rate=0.1):
    fps = 1 / sampling_rate
    image_files = sorted(glob.glob(os.path.join(input_folder, '*')))
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_path, codec='mpeg4')
def main():
    folder='capture'
    if not os.path.exists(folder):
        os.makedirs(folder)
    print("Preparing System to Capture Images")
    s = 0.1
    capture_images(0, s=s, t=10.0, folder=folder)
    destination_folder = 'features'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    print("Preparing to extract features...")
    for filename in tqdm(os.listdir(folder), desc="Extracting Features"):
        if filename.endswith('.jpg'):
            image_path = os.path.join(folder, filename)
            destination_path = os.path.join(destination_folder, filename.replace('.jpg', '_feature.jpg'))
            extract_features(image_path, destination_path)
    print("Images processed. Preparing to create videos...")   
    images_to_video('/home/users/u7143478/Desktop/dinov2/features', '/home/users/u7143478/Desktop/dinov2/feature_film.mp4', s)
    images_to_video('/home/users/u7143478/Desktop/dinov2/capture', '/home/users/u7143478/Desktop/dinov2/capture_film.mp4', s)
    print("Videos created. Cleaning up...")
    for filename in os.listdir(destination_folder):
        file_path = os.path.join(destination_folder, filename)
        os.remove(file_path)
    os.rmdir(destination_folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        os.remove(file_path)
    os.rmdir(folder)
    print("Concatenating videos...")
    feature_clip = VideoFileClip('/home/users/u7143478/Desktop/dinov2/feature_film.mp4')
    capture_clip = VideoFileClip('/home/users/u7143478/Desktop/dinov2/capture_film.mp4')
    final_clip = clips_array([[feature_clip, capture_clip]])
    final_clip.write_videofile('/home/users/u7143478/Desktop/dinov2/final_film.mp4')
    print("Video created---Cleaning up!")
    os.remove('/home/users/u7143478/Desktop/dinov2/feature_film.mp4')
    os.remove('/home/users/u7143478/Desktop/dinov2/capture_film.mp4')    
    video_path = '/home/users/u7143478/Desktop/dinov2/final_film.mp4'
    with VideoFileClip(video_path) as video:
        video_clip = video.subclip(0, 10)
        video_clip.write_videofile("output.mp4")
    output_path = "/home/users/u7143478/Desktop/dinov2/output.mp4" 
    print("Final Film captured!")
if __name__ == '__main__':
    main()
