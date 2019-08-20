import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from RecordPool import RecordPool


class BPMSupreme(RecordPool):
    def __init__(self):
        super().__init__("BPMSupreme", "BPMSUPREME")
        self.url = "https://www.bpmsupreme.com/store/newreleases/audio/smart"

        self.ignore = ("Short Edit", "Clean Short Edit", "Dirty Short Edit", "Quick Hit Clean", "Quick Hit")

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
            WebDriverWait(self.driver, 5).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, "tag"))
            )
        except TimeoutException:
            return tracks

        playlist = self.driver.find_element_by_class_name("genreslist")
        tags = playlist.find_elements_by_class_name("tag")
        num = number if number and len(tags) >= number else len(tags)
        for tag in tags[:num]:
            elements = tag.find_elements_by_xpath(".//*[@class='ng-binding ng-scope']")
            elements = [e for e in elements if e.text not in self.ignore]
            tracks.extend(elements)

        return tracks

    def next_page(self) -> bool:
        if self.driver.current_url != self.current_url:
            self.reload_page()

        try:
            element = WebDriverWait(self.driver, 5).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']"))
            )
            element.click()

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
