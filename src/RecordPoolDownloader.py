"""
Record Pool Downloader
Akseli Lukkarila
2019
"""

import logging
import os
import sys
import threading
import traceback

from Bandcamp import Bandcamp
from Beatjunkies import Beatjunkies
from BPMSupreme import BPMSupreme
from colorprint import print_bold, print_cyan, print_error, print_error_and_exit, print_red, print_yellow
from DJCity import DJCity
from RecordPool import RecordPool
from utils import Site


class RecordPoolDownloader:
    """Command line tool for recordpool web downloads."""

    def __init__(self, site: Site, url=""):
        if site == Site.BEATJUNKIES:
            self.pool = Beatjunkies()
        elif site == Site.BPMSUPREME:
            self.pool = BPMSupreme()
        elif site == Site.DJCITY:
            self.pool = DJCity()
        elif site == Site.BANDCAMP:
            self.pool = Bandcamp(url)
        else:
            raise RuntimeError(f"Unsupported record pool: {site}")

        self.pool.start_driver()
        logging.info(f"Initialized {self.pool} on {self.pool.system_name()}")
        logging.info(f"Download path: '{self.pool.download_path}'")

    def run_loop(self):
        """Start download loop with a specific mode."""
        print_bold("\nChoose mode:")
        print(" 0: Single page")
        print(">0: Multiple pages")
        try:
            number = int(input())
            print()
            if number > 0:
                self.multi_page_loop(number)
            else:
                self.single_page_loop()
        except ValueError:
            self.single_page_loop()

    def single_page_loop(self):
        """Download one page and ask to continue a single page at a time."""
        self.pool.update_current_page()
        while True:
            print_bold(f"--- Page: {self.pool.current_page_number} ---")
            try:
                number = int(input("Give number of tracks to download from current page (0 = all)\n"))
                number = max(0, number)
            except ValueError:
                number = 0

            self.single_page_download(number)
            if not self.pool.next_page():
                print_red("No more pages!")
                break

            self.play_notification_sound()
            if input("Continue?\n").lower() not in ("y", "1"):
                break

    def multi_page_loop(self, pages=1):
        """Download multiple pages automatically."""
        self.pool.update_current_page()
        last_page = self.pool.current_page_number + pages - 1
        for _ in range(1, pages + 1):
            print_bold(f"--- Page: {self.pool.current_page_number} / {last_page} ---")
            self.single_page_download()
            if not self.pool.next_page():
                print_red("No more pages!")
                return

        self.play_notification_sound()
        print_bold("Continue for pages?")
        try:
            num = int(input())
            if num > 0:
                self.multi_page_loop(num)
        except ValueError:
            return

    def single_page_download(self, num_to_download=0):
        """Download tracks from a single page."""
        tracks = self.pool.download_page(num_to_download)
        logging.info(f"Page {self.pool.current_page_number}: downloaded {tracks} files.")

    def play_notification_sound(self):
        """Play system notification sound without waiting for function call to finish."""
        threading.Thread(target=self._play_notification, args=(self.pool.platform.is_mac(),)).start()

    @staticmethod
    def _play_notification(mac: bool):
        if mac:
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        else:
            import winsound

            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

    def download_bandcamp_order(self):
        """Download Bandcamp order."""
        self.pool.download_page()
        self.pool.open_page("chrome://downloads/")
        input("Wait until downloads have finished and press a button...\n")


if __name__ == "__main__":
    print_cyan("RECORDPOOL DL", bold=True)
    args = sys.argv[1:]
    recordpool_site: Site | None = None
    # Try reading recordpool to use from first argument
    # TODO: use click or typer here for proper CLI handling
    site_name: str = args[0].strip() if args else None
    if "https://bandcamp.com/download" in site_name:
        recordpool_site = Site.BANDCAMP
    else:
        while not site_name:
            print_bold("\nChoose record pool:")
            # Get all pool implementations automatically
            pools: tuple[str] = tuple(pool.__name__ for pool in RecordPool.__subclasses__())
            options = dict(zip((str(i) for i in range(1, len(pools) + 1)), pools))
            # Arguably this would have been cleaner for the current options but wanted to make it generic and scalable
            # options = dict(zip(("1", "2", "3", "4"), ("Bandcamp", "Beatjunkies", "BPMSupreme", "DJCity")))
            for key, value in options.items():
                print(f"{key}: {value}")

            ans = input()
            if options.get(ans):
                site_name = options[ans]
            else:
                print_error("Give a valid option...")
        try:
            recordpool_site = Site[site_name.upper()]
        except KeyError:
            print_error_and_exit(f"Unsupported record pool: {site_name}")

    try:
        if recordpool_site == Site.BANDCAMP:
            url = site_name if site_name.startswith("https://") else input("\nGive Bandcamp download URL:\n")
            downloader = RecordPoolDownloader(recordpool_site, url=url)
            downloader.download_bandcamp_order()
        else:
            downloader = RecordPoolDownloader(recordpool_site)
            downloader.run_loop()
    except KeyboardInterrupt:
        print_bold("\nAborted")
        sys.exit()
    except Exception:
        logging.exception("Exception raised!")
        error_type, error_value, trace = sys.exc_info()
        print_error(error_type)
        if error_value:
            print_red(error_value)
        for line in traceback.format_tb(trace):
            print_yellow(line)
