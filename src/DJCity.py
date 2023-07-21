import random

from selenium.webdriver.common.by import By

from colorprint import Color, get_color, print_bold, print_color, print_yellow
from RecordPool import RecordPool
from utils import Site


class DJCity(RecordPool):
    def __init__(self):
        super().__init__(Site.DJCITY)
        self.url = "https://www.djcity.com/uk/digital/records.aspx?p=1"

        # pool specific
        self.filter = ""
        self.genres = ("hiphop", "house", "latin", "pop", "r&b", "reggae", "other")
        self.genre_map = dict(zip(self.genres, ("c1", "c2", "c3", "c4", "c5", "c6", "c8")))

    def get_tracks(self, number=0) -> list:
        playlist = self.driver.find_element(By.CSS_SELECTOR, ".float_left.page_left")
        links = playlist.find_elements(By.CSS_SELECTOR, ".downloadBtn")
        num = min(number, len(links)) if number > 0 else len(links)
        track_links = [url for url in (link.get_attribute("href") for link in links[:num]) if url]

        tracks = []
        total_pages = len(track_links)
        for page, link in enumerate(track_links, 1):
            print(f"{page} / {total_pages}", end="\r", flush=True)
            self.driver.get(link)
            # DJCity requires you to rate the song in order to download it
            if self.driver.find_elements(By.CSS_SELECTOR, ".rating-stars"):
                stars = self.driver.find_element(By.CSS_SELECTOR, ".rating-stars")
                stars.find_element(By.CSS_SELECTOR, f'[data-value="{random.randint(3, 5)}"]').click()
            else:
                # already reviewed -> skip
                continue

            downloads = self.driver.find_elements(By.CSS_SELECTOR, ".float_right.reviw_tdonw")
            for download in downloads:
                url = download.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                if url:
                    tracks.append(url)

        return tracks

    def get_page_number(self) -> int:
        link = self.current_url.replace("&", "=")
        digit = [int(s) for s in link.split("=") if s.isdigit()]
        return digit[0] if digit else 1

    def next_page(self) -> bool:
        self.current_page_number += 1
        url = f"https://www.djcity.com/uk/digital/records.aspx?p={self.current_page_number}{self.filter}"
        if url == self.current_url:
            return False

        self.driver.get(url)
        self.current_url = self.driver.current_url
        return True

    def prepare_pool(self):
        self.check_login()
        self.set_genre_filter()

    # Extra methods:
    def check_login(self):
        sign_in_element = self.driver.find_elements(by=By.LINK_TEXT("Sign In"))
        if sign_in_element:
            print("Not logged in, doing sign-in...\n")
            sign_in_element[0].click()
            self.driver.find_element_by_id("ctl00_PageContent_ctl00_ctrlLogin_LoginButton").click()
            # Make sure we are on correct page after logging in
            if self.driver.current_url != self.url:
                self.driver.get(self.url)

    def set_genre_filter(self):
        genres = ("hiphop", "house", "r&b", "pop", "other")
        print_bold("Use default genres (y/n)?")
        if input().lower() in ("n", "no", "0"):
            print_bold("Choose genres:")
            print_color("hiphop, house, r&b, latin, pop, reggae, other", Color.cyan)
            genres = [genre for genre in (i.strip().lower() for i in input().split(",")) if genre in self.genres]
            if not genres:
                print("No genres specified, using all...")
                return

        print(f"Genres: {get_color(', '.join(genres), Color.yellow)}")
        self.filter = "&f=ddfilter"
        for genre in genres:
            genre_id = self.genre_map.get(genre.lower())
            if genre_id:
                self.filter += f"&{genre_id}=on"
            else:
                print_yellow(f"Skipping invalid genre: '{genre}'")

        self.current_url = f"https://www.djcity.com/uk/digital/records.aspx?p={self.current_page_number}"
        self.current_url += self.filter
        self.driver.get(self.current_url)
