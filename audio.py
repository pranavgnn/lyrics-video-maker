from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pytubefix import YouTube
import librosa

class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_link(self, artist, title):
        query = f"{artist}+{title}".replace(" ", "+")
        self.driver.get(f"https://www.youtube.com/results?search_query={query}+lyrics")
        link = self.driver.find_element(By.XPATH, "//a[starts-with(@href, \"/watch?v=\")]")
        return link.get_attribute("href").split("&")[0] if link else None

    def close(self):
        self.driver.quit()

class AudioFetcher:
    def __init__(self):
        self.scraper = Scraper()

    def fetch_audio(self, artist, title):
        link = self.scraper.get_link(artist, title)
        print(link)

        if link:
            yt = YouTube(link)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(filename=f"audio")

    
    def get_bpm(self):
        y, sr = librosa.load("audio.m4a")
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return tempo.round(2)


    def close(self):
        self.scraper.close()