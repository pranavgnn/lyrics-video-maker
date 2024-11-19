from PIL import Image, ImageDraw, ImageFont
import threading
import os

from lyrics import LyricsFetcher

class ImageMaker:
    def __init__(self, lyrics : list[dict]):
        self.lyrics = lyrics
        self.folder = "lyrics_images"

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        else:
            for file in os.listdir(self.folder):
                os.remove(os.path.join(self.folder, file))


    def make_image(self, line):
        timestamp = line["timestamp"]
        line = line["line"].upper()

        background = Image.open("../background.jpg")
        width, height = background.size

        font = ImageFont.truetype("../LilitaOne-Regular.ttf", int(0.085 * width)) # 8.5% of width

        draw = ImageDraw.Draw(background)

        margin = 150
        wrapped_line = ""

        for word in line.split():
            if font.getbbox(wrapped_line.split("\n")[-1] + word)[2] > width - margin * 2:
                wrapped_line += "\n"
            wrapped_line += word + " "

        wrapped_line = wrapped_line.strip()
        rows = wrapped_line.split("\n")

        centered_rows = []

        for row in rows:
            # row = (" " * (max([len(r) for r in rows]) // 2 - len(row) // 2)) + row
            row = row.center(max([len(r) for r in rows]))
            centered_rows.append(row)
        
        wrapped_line = "\n".join(centered_rows)

        _, _, w, h = draw.textbbox((0, 0), wrapped_line, font=font)
        draw.text(((width-w)/2, (height-h)/2), wrapped_line, font=font, fill=(255, 255, 255))

        background.save(f"{self.folder}/lyrics_{timestamp}.jpg")

    def make_images(self):
        threads = []

        for line in self.lyrics:
            thread = threading.Thread(target=self.make_image, args=(line,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    fetcher = LyricsFetcher("Lady Gaga", "Die With A Smile")
    fetcher.fetch_lyrics()

    maker = ImageMaker(fetcher.get_lyrics())
    maker.make_images()
