import logging
import os
import shutil
import time

from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.service import Service as ChromeService
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from colorprint import Color, get_color, print_color, print_error_and_exit, print_magenta, print_red
from utils import Platform, Site


class RecordPool:
    """Parent class for all recordpool implementations."""

    def __init__(self, site: Site, download_folder_name: str = None):
        self.current_page_number: int = 0
        self.current_url: str = ""
        self.driver: webdriver = None
        self.folder: str = download_folder_name if download_folder_name else site.name
        self.name = str(site)
        self.platform: Platform = Platform.get()
        self.site: Site = site
        self.total_files_downloaded: int = 0
        self.url: str = ""

        # Setup log file and format
        logging.basicConfig(
            filename=f"{self.name}.log",
            filemode="w",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
        )

        # TODO: use Pathlib instead of os.path
        user_path = os.path.expanduser("~")
        if self.platform.is_linux():
            print_error_and_exit("Linux is not yet supported")

        if self.platform.is_mac():
            download_root = os.path.join(user_path, "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, r"Library/Application Support/Google/Chrome")
        elif self.platform.is_windows():
            download_root = os.path.join("D:\\", "Dropbox", "DJ MUSIC SORT")
            chrome_profile = os.path.join(user_path, "AppData\\Local\\Google\\Chrome\\User Data")

        self.download_path = os.path.join(download_root, self.folder)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path, exist_ok=True)

        self.free_space_at_start, _ = self.free_disk_space()

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument(f"user-data-dir={chrome_profile}")
        self.chrome_options.add_argument("profile-directory=Default")
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

    def check_free_disk_space(self, limit_in_mb=1024) -> bool:
        """Check that there is more free disk space left than the given limit. Default is 1024 megabytes."""
        free, ratio = self.free_disk_space()
        logging.debug(f"free disk space: {free:.1f} MB ({ratio:.1%})")
        return free > limit_in_mb

    def download_page(self, num_to_download=0) -> int:
        """Download all main files on current page, or optionally only the "num_to_download" first tracks."""
        if not self.check_free_disk_space():
            raise OSError("Disk is full!")

        print_magenta("Getting download links...")
        tracks = self.get_tracks(num_to_download)
        if not tracks:
            print_red("No files to download!\n")
            return 0

        print_magenta("Downloading files...")
        # tqdm creates a progress bar
        for track in tqdm(tracks):
            self.download(track)

        # wait a bit for downloads to finish
        time.sleep(2)
        num_tracks = len(tracks)
        self.total_files_downloaded += num_tracks
        return num_tracks

    def download(self, track):
        """Download one track."""
        # Default implementation. Override if needed.
        self.driver.get(track)

    def free_disk_space(self) -> tuple[int, float]:
        """Returns free disk space in download path as a tuple of megabytes and ratio of free space left."""
        total, _, free = shutil.disk_usage(self.download_path)
        free_mb = free / (1024 * 1024)
        free_ratio = free / total
        return free_mb, free_ratio

    def get_page_number(self) -> int:
        """Get the current page number."""
        # Default implementation. Override if needed.
        digits = [int(s) for s in self.current_url.split("/") if s.isdigit()]
        page = digits[0] if digits else 1
        return page

    def get_tracks(self, number=0) -> list:
        """Return a list of track objects that can be downloaded."""
        # Override in site-specific child class.
        raise NotImplementedError

    def next_page(self) -> bool:
        """Load next page, or return false if there are no more pages available."""
        # Override in site-specific child class.
        raise NotImplementedError

    def open_page(self, url):
        """Open given url."""
        self.driver.get(url)
        self.update_current_page()

    def prepare_pool(self):
        """Additional pool setup if needed, such as selecting genres."""
        pass

    def print_stats(self):
        """Print download statistics."""
        print("--------------------")
        print_color(self.name, Color.cyan)
        free_space, _ = self.free_disk_space()
        total_size = self.free_space_at_start - free_space
        msg = f"Total files downloaded: {self.total_files_downloaded} / {total_size:.1f} MB"
        logging.info(msg)
        print(msg, end="\n\n")

    def reload_page(self):
        """Reload currently stored page url."""
        self.driver.get(self.current_url)

    def set_start_page(self, page_number):
        """Set current page number to given number."""
        self.current_page_number = page_number

    def start_driver(self):
        """Open webdriver and prepare pool for downloading."""
        print_magenta("Starting ChromeDriver...")
        try:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options
            )
            self.driver.implicitly_wait(0.5)
            self.driver.get(self.url)
            self.current_url = self.driver.current_url
        except InvalidArgumentException:
            print_error_and_exit("\nError: Chrome already running. Close Chrome and try again...")

        print(f"\n{repr(self)}")
        self.prepare_pool()

    def update_current_page(self):
        """Update page variables (url and page number) to match currently loaded page."""
        self.current_url = self.driver.current_url
        self.current_page_number = self.get_page_number()

    def quit(self):
        """Close driver and print download stats."""
        if self.driver:
            self.driver.quit()
            self.print_stats()

    def system_name(self) -> str:
        """Returns a formatted string for the platform name."""
        return repr(self.platform)

    def __str__(self):
        return self.name

    def __repr__(self):
        free, ratio = self.free_disk_space()
        text = "pool: " + get_color(f"{self.name}\n", Color.cyan)
        text += f"path: {get_color(self.download_path, Color.yellow)}\n"
        text += f"disk: {free / 1024:.1f} GB ({ratio:.1%}) free"
        return text

    def __del__(self):
        """Clean up webdriver and print stats automatically when quitting."""
        self.quit()
