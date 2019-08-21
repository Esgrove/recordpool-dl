import random

from colorprint import printColor, printBold, getColor, Color
from RecordPool import RecordPool


class DJCity(RecordPool):
    def __init__(self):
        super().__init__("DJCity", "DJCITY")
        self.url = "https://www.djcity.com/uk/digital/records.aspx?p=1"

        self.filter = ""
        self.genres = ("hiphop", "house", "latin", "pop", "r&b", "reggae", "other")
        self.genre_map = dict(zip(self.genres, ("c1", "c2", "c3", "c4", "c5", "c6", "c8")))

    def get_tracks(self, number=0) -> list:
        playlist = self.driver.find_element_by_css_selector(".float_left.page_left")
        links = playlist.find_elements_by_css_selector(".downloadBtn")
        num = min(number, len(links)) if number > 0 else len(links)
        track_links = []
        for link in links[:num]:
            url = link.get_attribute("href")
            if url:
                track_links.append(url)

        tracks = []
        total_pages = len(track_links)
        for page, link in enumerate(track_links, 1):
            print(f"{page} / {total_pages}", end="\r", flush=True)
            self.driver.get(link)
            if self.driver.find_elements_by_css_selector('.rating-stars'):
                stars = self.driver.find_element_by_css_selector(".rating-stars")
                stars.find_element_by_css_selector(f"[data-value=\"{random.randint(3, 5)}\"]").click()
            else:
                # already reviewed -> skip
                continue

            downloads = self.driver.find_elements_by_css_selector(".float_right.reviw_tdonw")
            for download in downloads:
                url = download.find_element_by_css_selector('a').get_attribute('href')
                if url:
                    tracks.append(url)

        return tracks

    def get_page_number(self) -> int:
        link = self.current_url.replace("&", "=")
        digit = [int(s) for s in link.split("=") if s.isdigit()]
        if digit:
            return digit[0]
        else:
            return 1

    def next_page(self) -> bool:
        self.current_num += 1
        url = f"https://www.djcity.com/uk/digital/records.aspx?p={self.current_num}{self.filter}"
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
        sign_in = self.driver.find_elements_by_link_text("Sign In")
        if sign_in:
            print("Not logged in, doing sign in...\n")
            sign_in[0].click()
            self.driver.find_element_by_id("ctl00_PageContent_ctl00_ctrlLogin_LoginButton").click()
            if self.driver.current_url != self.url:
                self.driver.get(self.url)

    def set_genre_filter(self):
        printBold("Use default genres (y/n)?")
        ans = input()
        if ans.lower() in ("n", "no", "0"):
            printBold("Choose genres:")
            printColor("hiphop, house, r&b, latin, pop, reggae, other", Color.cyan)
            genres = [i.strip().lower() for i in input().split(",") if i.strip().lower() in self.genres]
            if not genres:
                print("No genres specified, using all...")
                return

        else:
            genres = ("hiphop", "house", "r&b", "pop", "other")

        print("Genres: {}".format(getColor(", ".join(genres), Color.yellow)))
        self.filter = "&f=ddfilter"
        for genre in genres:
            genre_id = self.genre_map[genre.lower()]
            self.filter += f"&{genre_id}=on"

        self.current_url = f"https://www.djcity.com/uk/digital/records.aspx?p={self.current_num}"
        self.current_url += self.filter
        self.driver.get(self.current_url)
