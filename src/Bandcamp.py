import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from RecordPool import RecordPool
from colorprint import Color, print_color


class Bandcamp(RecordPool):
    def __init__(self):
        super().__init__(self.__class__.__name__, "BANDCAMP")
        self.url = input("\nGive download URL:\n")

    def download(self, track):
        self.driver.get(track)
        time.sleep(1)

    def download_page(self, number=0) -> int:
        # overridden to directly download files without using 'get_tracks'
        if not self.check_free_disk_space():
            raise OSError("Disk is full!")

        downloads = self.driver.find_elements_by_class_name("downloads")
        if not downloads:
            raise RuntimeError("No downloads found")

        print_color("downloading files...", Color.yellow)
        tracks = downloads[0].find_elements_by_class_name("download-title")
        # TODO: get download links using async tasks instead of sequentially to speedup download
        for song in tqdm(tracks):
            # wait for Bandcamp to prepare download
            button = WebDriverWait(song, 600).until(EC.element_to_be_clickable((By.CLASS_NAME, "item-button")))
            url = button.get_attribute("href")
            self.download(url)

        # wait a bit for downloads to finish
        time.sleep(2)
        num_tracks = len(tracks)
        self.total_files_downloaded += num_tracks
        return num_tracks

    def get_tracks(self, number=0) -> list:
        # not needed
        return []

    def next_page(self) -> bool:
        # not needed
        return False

    def prepare_pool(self):
        # expand downloads if needed
        elements = self.driver.find_elements_by_class_name("bfd-download-dropdown")
        if elements:
            elements[0].click()
