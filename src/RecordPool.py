import logging
import os
import time
import sys
import shutil
import platform

from tqdm import tqdm

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from colorprint import Color, get_color, print_color


class RecordPool:
    """ Parent class for all recordpool implementations."""
    def __init__(self, name, folder_name):
        self.name = name
        self.folder = folder_name
        self.system = platform.system().lower()
        self.current_url = None
        self.current_num = None
        self.driver = None
        self.total_tracks = 0
        self.url = ""

        user_path = os.path.expanduser("~")
        if self.windows():
            download_root = os.path.join(user_path, "Downloads") # os.path.join("D:\\", "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, "AppData\\Local\\Google\\Chrome\\User Data")
            self.chrome_driver = "D:\\Dropbox\\CODE\\webdriver\\chromedriver.exe"

        elif self.mac_os():
            download_root = os.path.join(user_path, "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, r"Library/Application Support/Google/Chrome")
            self.chrome_driver = "/usr/local/bin/chromedriver"

        else:
            print_color(f"Unsupported OS: '{platform.system()}'", Color.red)
            sys.exit()

        self.download_path = os.path.join(download_root, self.folder)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("user-data-dir=" + chrome_profile)
        self.chrome_options.add_argument("profile-directory=Default")
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True})

        logging.basicConfig(filename=f"{self.name}.log", filemode='w', level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s', datefmt="%Y.%m.%d %H:%M:%S")

    def check_free_disk_space(self, limit_in_mb=1024) -> bool:
        """Check that there is more free disk space left than the given limit. Default is 1024 megabytes."""
        total, _, free = shutil.disk_usage(self.download_path)
        free_mb = free / 1048576  # 1024^2
        logging.debug(f"free disk space: {free_mb} MB ({free / total:.1%})")
        return free_mb > limit_in_mb

    def download_page(self, number=0) -> int:
        """ Download all main files on current page, or optionally only the "number" first tracks."""
        if not self.check_free_disk_space():
            raise OSError("Disk is full!")

        print_color("Getting download links...", Color.yellow)
        tracks = self.get_tracks(number)
        if not tracks:
            print_color("No files to download!\n", Color.red)
            return 0

        print_color("downloading files...", Color.yellow)
        for track in tqdm(tracks):
            self.download(track)

        # wait a bit for downloads
        time.sleep(2)

        num_tracks = len(tracks)
        self.total_tracks += num_tracks
        return num_tracks

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
        self.update_current_page()

    def prepare_pool(self):
        # Override if needed.
        pass

    def print_stats(self):
        print("--------------------")
        print_color(self.name, Color.cyan)
        msg = f"Total files downloaded: {self.total_tracks}"
        print(msg, end="\n\n")
        logging.info(msg)

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
            print_color("\nError: Chrome already running. Close Chrome and try again...", Color.red)
            sys.exit()

        print(f"\nDownloader initialized for:\n{repr(self)}")

        self.prepare_pool()

    def update_current_page(self):
        self.current_url = self.driver.current_url
        self.current_num = self.get_page_number()

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.print_stats()

    def mac_os(self) -> bool:
        return self.system == "darwin"

    def windows(self) -> bool:
        return self.system == "windows"

    def system_name(self) -> str:
        if self.mac_os():
            return f"MacOS {platform.mac_ver()[0]}"
        else:
            return f"Windows {platform.win32_ver()[0]} {platform.win32_ver()[1].split('.')[-1]}"

    def __str__(self):
        return self.name

    def __repr__(self):
        text = get_color(f"/// {self.name} ///\n", Color.cyan)
        text += f"--> {get_color(self.download_path, Color.yellow)}"
        return text

    def __del__(self):
        self.quit()
