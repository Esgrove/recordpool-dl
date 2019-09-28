import time

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
        songs = self.driver.find_elements_by_class_name("download-title")
        for song in songs:
            button = WebDriverWait(song, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "item-button")))
            url = button.get_attribute("href")
            tracks.append(url)

        return tracks

    def next_page(self) -> bool:
        # not needed
        return False

    def prepare_pool(self):
        # expand downloads if needed
        elements = self.driver.find_elements_by_class_name("bfd-download-dropdown")
        if elements:
            elements[0].click()
