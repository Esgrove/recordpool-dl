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
        super().__init__(self.__class__.__name__, "BPMSUPREME")
        self.url = "https://app.bpmsupreme.com/new-releases/classic/audio"
        self.wait_time = 10
        self.track_ignore = ("Short Edit",
                             "Clean Short Edit",
                             "Dirty Short Edit",
                             "Quick Hit Clean",
                             "Quick Hit",
                             "Quick Hit Dirty")

        self.genre_ignore = ("Alternative",
                             "Bachata",
                             "Banda",
                             "Country",
                             "Corrido",
                             "Cumbia",
                             "Cumbias",
                             "Dancehall",
                             "Dembow",
                             "Drum Loops",
                             "Latin Pop",
                             "Mambo",
                             "Mariachi",
                             "Norteno",
                             "Reggae",
                             "Reggaeton",
                             "Rock",
                             "Salsa",
                             "Scratch Tools",
                             "Soca")

    def click(self, element):
        self.driver.execute_script("arguments[0].click()", element)

    def close_error_popup(self):
        elements = self.driver.find_elements_by_xpath(".//*[@class='sweet-alert showSweetAlert visible']")
        if elements:
            button = elements[0].find_element_by_class_name("confirm")
            self.click(button)
            time.sleep(0.5)

    def download(self, track):
        try:
            self.click(track)
            # give download a bit of time to start before returning
            time.sleep(0.6)
        except StaleElementReferenceException:
            return

    def get_page_number(self) -> int:
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "pagination")))
        container = self.driver.find_element_by_class_name("pagination")
        page = container.find_element_by_class_name("selected")
        number = int(page.text)
        return number

    def get_tracks(self, number=0) -> list:
        tracks = []
        try:
            # wait for songs to load
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "table-media")))
        except TimeoutException:
            print(f"No tracks found after waiting for {self.wait_time} seconds...")
            return tracks

        playlist = self.driver.find_element_by_class_name("table-media")
        songs = playlist.find_elements_by_class_name("row-container")
        num_max = min(number, len(songs)) if number > 0 else len(songs)
        for song in songs[:num_max]:
            genre = song.find_element_by_xpath(".//*[@class='col-category link']")
            if genre.text in self.genre_ignore:
                continue

            tag = song.find_element_by_class_name("row-tags")
            elements = tag.find_elements_by_xpath(".//*[@class='tag-view ']")
            filtered = [e for e in elements if e.text not in self.track_ignore]
            if filtered:
                tracks.extend(filtered)

        return tracks

    def next_page(self) -> bool:
        self.close_error_popup()
        if self.driver.current_url != self.current_url:
            self.reload_page()

        container = self.driver.find_element_by_class_name("pagination")
        try:
            element = container.find_element_by_xpath("//*[contains(text(), '›')]")
            self.click(element)

        except (ElementNotInteractableException, ElementClickInterceptedException, TimeoutException):
            return False

        self.update_current_page()
        return True

    def prepare_pool(self):
        input("Choose genres manually and press a key to continue...")


