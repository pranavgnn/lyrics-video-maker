import requests

class LyricsFetcher:
    def __init__(self, artist: str, title: str):
        self.artist = "+".join(artist.split())
        self.title = "+".join(title.split())

    def fetch_lyrics(self):
        url = f"https://lrclib.net/api/get?artist_name={self.artist}&track_name={self.title}"
        response = requests.get(url)
        data = response.json()

        synced_lyrics = data["syncedLyrics"].split("\n")
        formatted_lyrics = []

        for line in synced_lyrics:
            split_line = line.strip()[1:].split("] ")
            if len(split_line) == 1:
                split_line[0] = split_line[0][:-1]

            timestamp = split_line[0]
            line = split_line[1] if len(split_line) == 2 else ""

            mins, sec = map(float, timestamp.split(":"))
            formatted_lyrics.append({
                "timestamp": mins * 60 + sec,
                "line": line
            })

        self.lyrics = formatted_lyrics

        return formatted_lyrics

    def get_lyrics(self):
        return self.lyrics
    
if __name__ == "__main__":
    fetcher = LyricsFetcher("Lady Gaga", "Die With A Smile")
    fetcher.fetch_lyrics()

    with open("out.json", "w") as f:
        f.write(str(fetcher.get_lyrics()))