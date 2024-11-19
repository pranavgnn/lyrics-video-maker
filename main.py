import os
from video import LyricsFetcher, AudioFetcher, ImageMaker, VideoMaker

artist_name = "Lady Gaga"
song_title = "Die With A Smile"
folder_name = f"{artist_name} - {song_title}"

if not os.path.exists(folder_name):
    os.mkdir(folder_name)

os.chdir(folder_name)

print(f"Making video for {artist_name} - {song_title}...")

print("Fetching lyrics...")
lyrics_fetcher = LyricsFetcher(artist_name, song_title)
lyrics_fetcher.fetch_lyrics()
print("Lyrics fetched!")

print("Fetching audio...")
audio_fetcher = AudioFetcher()
audio_fetcher.fetch_audio(artist_name, song_title)
print("Audio fetched!")

bpm = audio_fetcher.get_bpm()
print("Song BPM:", bpm)

print("Making images...")
images_maker = ImageMaker(lyrics_fetcher.get_lyrics())
images_maker.make_images()
print("Images made!")

print("Making video...")
video_maker = VideoMaker(images_maker.folder, bpm)
video_maker.make_video()
video_maker.add_audio()
print("Video made!")