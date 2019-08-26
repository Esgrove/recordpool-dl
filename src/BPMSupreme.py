import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from RecordPool import RecordPool


class BPMSupreme(RecordPool):
    def __init__(self):
        super().__init__("BPMSupreme", "BPMSUPREME")
        self.url = "https://www.bpmsupreme.com/store/newreleases/audio/classic/1"

        self.track_ignore = ("Short Edit",
                             "Clean Short Edit",
                             "Dirty Short Edit",
                             "Quick Hit Clean",
                             "Quick Hit",
                             "Quick Hit Dirty")

        self.genre_ignore = ("Alternative",
                             "Country",
                             "Dancehall",
                             "Dembow",
                             "Drum Loops",
                             "Latin Pop",
                             "Reggae",
                             "Reggaeton",
                             "Rock",
                             "Salsa",
                             "Scratch Tools",
                             "Soca")

    def download(self, track):
        try:
            self.driver.execute_script("arguments[0].click()", track)
        except StaleElementReferenceException:
            return

        time.sleep(0.5)

    def get_tracks(self, number=0) -> list:
        tracks = []
        try:
            # wait for songs to load
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "tag")))
        except TimeoutException:
            return tracks

        playlist = self.driver.find_element_by_class_name("genreslist")
        songs = playlist.find_elements_by_class_name("track_bx")
        num_max = min(number, len(songs)) if number > 0 else len(songs)
        for song in songs[:num_max]:
            genre = song.find_element_by_xpath(".//*[@class='cat ng-binding']")
            if genre.text in self.genre_ignore:
                continue

            tag = song.find_element_by_class_name("tag")
            elements = tag.find_elements_by_xpath(".//*[@class='ng-binding ng-scope']")
            elements = [e for e in elements if e.text not in self.track_ignore]
            tracks.extend(elements)

        return tracks

    def next_page(self) -> bool:
        if self.driver.current_url != self.current_url:
            self.reload_page()

        try:
            element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
            self.driver.execute_script("arguments[0].click()", element)

        except (ElementNotInteractableException, ElementClickInterceptedException, TimeoutException):
            self.current_num += 1
            parts = re.split("(\\d+)", self.driver.current_url)
            parts[1] = str(self.current_num)
            next_page = "".join(parts)
            self.driver.get(next_page)

        self.update_current_page()
        return True

    def prepare_pool(self):
        input("Choose genres manually and press a key to continue...\n")
