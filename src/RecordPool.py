import os
import sys
import platform

from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from colorprint import printColor, getColor, Color


class RecordPool:
    """ Parent class for all recordpool-specific implementations."""
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.current_url = None
        self.current_num = None
        self.driver = None
        self.total_tracks = 0
        self.url = ""

        user_path = os.path.expanduser("~")
        if platform.system().lower() == "windows":
            download_root = os.path.join("D:\\", "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, "AppData\\Local\\Google\\Chrome\\User Data")
            self.chrome_driver = "C:\\ProgramData\\chocolatey\\bin\\chromedriver.exe"

        elif platform.system().lower() == "darwin":
            download_root = os.path.join(user_path, "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, r"Library/Application Support/Google/Chrome")
            self.chrome_driver = "/usr/local/bin/chromedriver"

        else:
            printColor(f"Unsupported OS \"{platform.system()}\"", Color.red)
            sys.exit()

        self.download_path = os.path.join(download_root, self.folder)

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("user-data-dir=" + chrome_profile)
        self.chrome_options.add_argument("profile-directory=Default")
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True})

    def download_page(self, number=0):
        """ Download all main files on current page, or optionally only the "number" first tracks."""
        printColor("Getting download links...", Color.yellow)
        tracks = self.get_tracks(number)

        if not tracks:
            printColor("No files to download!\n", Color.red)
            return

        printColor("downloading files...", Color.yellow)
        for track in tqdm(tracks):
            self.download(track)

        self.total_tracks += len(tracks)
        printColor("Done!\n", Color.green)

    def download(self, track):
        # Default implementation. Override if needed.
        self.driver.get(track)

    def get_page_number(self) -> int:
        # Default implementation. Override if needed.
        digits = [int(s) for s in self.current_url.split("/") if s.isdigit()]
        page = 1 if not digits else digits[0]
        return page

    def get_tracks(self, number=0) -> list:
        # Override in site-spesific child class.
        raise NotImplementedError

    def next_page(self) -> bool:
        # Override in site-spesific child class.
        raise NotImplementedError

    def open_page(self, url):
        self.driver.get(url)
        self.update_current_page

    def prepare_pool(self):
        # Override if needed.
        pass

    def print_stats(self):
        print("--------------------")
        printColor(self.name, Color.cyan)
        print(f"Total files downloaded: {self.total_tracks}\n")

    def reload_page(self):
        self.driver.get(self.current_url)

    def set_start_page(self, page_number):
        self.current_num = page_number

    def start_driver(self):
        try:
            self.driver = webdriver.Chrome(executable_path=self.chrome_driver, options=self.chrome_options)
            self.driver.implicitly_wait(0.5)
            self.driver.get(self.url)
            self.current_url = self.driver.current_url

        except InvalidArgumentException:
            printColor("\nError: Chrome already running. Close Chrome and try again...", Color.red)
            sys.exit()

        print("\nDownloader initialized for:\n" + repr(self))

        self.prepare_pool()

    def update_current_page(self):
        self.current_url = self.driver.current_url
        self.current_num = self.get_page_number()

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.print_stats()

    def __str__(self):
        return self.name

    def __repr__(self):
        text = getColor(f"/// {self.name} ///\n", Color.cyan)
        text += f"--> {getColor(self.download_path, Color.yellow)}"
        return text

    def __del__(self):
        self.quit()
