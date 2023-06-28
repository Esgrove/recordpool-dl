import logging
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from colorprint import Color, print_color, print_error, print_magenta, print_yellow
from RecordPool import RecordPool
from utils import Site


class Bandcamp(RecordPool):
    def __init__(self, url):
        super().__init__(Site.BANDCAMP)
        self.url = url

    def download(self, track):
        for _ in range(3):
            try:
                self.driver.get(track)
                time.sleep(2)
                break
            except Exception as e:
                print(e)

            time.sleep(10)

    def download_page(self, num_to_download=0) -> int:
        # overridden to directly download files without using 'get_tracks'
        if not self.check_free_disk_space():
            raise OSError("Disk is full!")

        print_magenta("Getting download links...")

        downloads = self.driver.find_elements(by=By.CLASS_NAME, value="downloads")
        if not downloads:
            print_error("No downloads found. Something is probably broken...")
            sys.exit(1)

        tracks = downloads[0].find_elements(by=By.CLASS_NAME, value="download-title")
        if not tracks:
            print_error("No items to download. Something is probably broken...")
            sys.exit(1)

        print_yellow(f"Found {len(tracks)} items")

        print_magenta("Downloading...")
        # TODO: get download links using async tasks instead of sequentially to speedup download
        for song in tqdm(tracks, unit="item"):
            # wait for Bandcamp to prepare download
            button = WebDriverWait(song, 600).until(
                expected_conditions.element_to_be_clickable((By.CLASS_NAME, "item-button"))
            )
            url = button.get_attribute("href")
            logging.debug(f"url: {url}")
            self.download(url)

        # wait a bit for downloads to finish
        time.sleep(1)
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
        logging.info("Checking to expand downloads...")
        self.driver.implicitly_wait(10)
        elements = self.driver.find_elements(by=By.CLASS_NAME, value="bfd-download-dropdown")
        if elements:
            logging.info("Expanding downloads...")
            elements[0].click()
        else:
            logging.info("Download expand element not found")
