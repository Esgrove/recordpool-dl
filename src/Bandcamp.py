import time

from colorprint import Color, print_color
from RecordPool import RecordPool

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Bandcamp(RecordPool):
    def __init__(self):
        super().__init__("Bandcamp", "#SORT")
        self.url = input("\nGive download URL:\n")

    def download(self, track):
        self.driver.get(track)
        time.sleep(1)

    def get_tracks(self, number=0) -> list:
        tracks = []
        downloads = self.driver.find_elements_by_class_name("downloads")
        if not downloads:
            raise RuntimeError("No downloads found")

        # TODO: async get download links
        songs = downloads[0].find_elements_by_class_name("download-title")
        for number, song in enumerate(songs, 1):
            print(f"  {number}:", end=" ")
            # wait for Bandcamp to prepare download
            button = WebDriverWait(song, 300).until(EC.element_to_be_clickable((By.CLASS_NAME, "item-button")))
            url = button.get_attribute("href")
            tracks.append(url)
            print_color("X", Color.green)

        return tracks

    def next_page(self) -> bool:
        # not needed
        return False

    def prepare_pool(self):
        # expand downloads if needed
        elements = self.driver.find_elements_by_class_name("bfd-download-dropdown")
        if elements:
            elements[0].click()
