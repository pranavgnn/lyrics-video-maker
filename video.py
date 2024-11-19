from moviepy.editor import VideoFileClip, AudioFileClip
import cv2
import os
import numpy as np

from images import LyricsFetcher, ImageMaker
from audio import AudioFetcher

def get_sway_offsets(bpm, time):
    speed = 4
    frequency = bpm / 60.0 / speed
    amplitude_x = 5
    amplitude_y = 2.5
    sway_x = amplitude_x * np.sin(2 * np.pi * frequency * time)
    sway_y = amplitude_y * np.cos(2 * np.pi * frequency * time)
    return sway_x, sway_y

def get_zoom_scale(bpm, time, min_zoom=1.0, max_zoom=1.03):
    beats_per_second = bpm / 60.0
    beat_duration = 1.0 / beats_per_second
    time_within_beat = time % beat_duration

    sharpness = 8
    decay_rate = 3 

    if time_within_beat < beat_duration / 4:
        zoom_factor = min_zoom + (max_zoom - min_zoom) * (time_within_beat * sharpness)
    else:
        decay_time = time_within_beat - beat_duration / 4
        zoom_factor = max_zoom - (max_zoom - min_zoom) * (decay_time * decay_rate / beat_duration)

    zoom_factor = max(min_zoom, min(max_zoom, zoom_factor))

    return float(zoom_factor)

class VideoMaker:
    def __init__(self, folder, bpm):
        self.folder = folder
        self.bpm = bpm
        self.video_name = "output.avi"
        self.audio_file = "audio.m4a"
        self.fps = 30

    def add_img(self, video, img, current_timestamp, width, height, total_frames):
        for frame_idx in range(total_frames):
            time = current_timestamp + frame_idx / self.fps
            sway_x, sway_y = get_sway_offsets(self.bpm, time)
            zoom_scale = get_zoom_scale(self.bpm, time)

            sway_x = float(sway_x)
            sway_y = float(sway_y)
            zoom_scale = float(zoom_scale)

            center_x, center_y = width / 2, height / 2

            transformation_matrix = np.float32([
                [zoom_scale, 0, (1 - zoom_scale) * center_x],
                [0, zoom_scale, (1 - zoom_scale) * center_y]
            ])

            swayed_img = cv2.warpAffine(img, transformation_matrix, (width, height))

            M = np.float32([[1, 0, sway_x], [0, 1, sway_y]])
            swayed_img = cv2.warpAffine(swayed_img, M, (width, height))

            video.write(swayed_img)

    def make_video(self):
        images = [img for img in os.listdir(self.folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

        frame = cv2.imread("../background.jpg")
        height, width, _ = frame.shape

        fps = 30
        video = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

        if images[0].split("_")[1].split(".")[0] != "0":
            self.add_img(video, frame, 0, width, height, int(images[0].split("_")[1].split(".")[0]) * fps) 

        for idx in range(len(images)):
            current_timestamp = int(images[idx].split("_")[1].split(".")[0])

            if idx < len(images) - 1:
                next_timestamp = int(images[idx + 1].split("_")[1].split(".")[0])
            else:
                next_timestamp = current_timestamp + 4

            duration = next_timestamp - current_timestamp
            total_frames = duration * fps

            img = cv2.imread(os.path.join(self.folder, images[idx]))

            self.add_img(video, img, current_timestamp, width, height, total_frames)

        video.release()


    def add_audio(self):
        video_clip = VideoFileClip(self.video_name)
        audio_clip = AudioFileClip(self.audio_file)

        final_video = video_clip.set_audio(audio_clip)

        final_video_name = "output_with_audio.mp4"
        final_video.write_videofile(final_video_name, codec='libx264', audio_codec='aac')

        video_clip.close()
        audio_clip.close()


if __name__ == "__main__":
    artist = "Lady Gaga"
    title = "Die With A Smile"

    lyrics_fetcher = LyricsFetcher(artist, title)
    lyrics_fetcher.fetch_lyrics()

    audio_fetcher = AudioFetcher()
    audio_fetcher.fetch_audio(artist, title)
    bpm = audio_fetcher.get_bpm()

    images_maker = ImageMaker(lyrics_fetcher.get_lyrics())
    images_maker.make_images()

    maker = VideoMaker(images_maker.folder, bpm)
    maker.make_video()
    maker.add_audio()