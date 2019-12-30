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

from colorprint import Color, print_bold, print_color

from Bandcamp import Bandcamp
from Beatjunkies import Beatjunkies
from BPMSupreme import BPMSupreme
from DJCity import DJCity


class RecordPoolDownloader:
    """Command line tool for recordpool web downloads."""
    def __init__(self, site: str):
        if site == "beatjunkies":
            self.pool = Beatjunkies()
        elif site == "bpmsupreme":
            self.pool = BPMSupreme()
        elif site == "djcity":
            self.pool = DJCity()
        elif site == "bandcamp":
            self.pool = Bandcamp()
        else:
            raise RuntimeError(f"Unsupported record pool: {site}!")

        self.pool.start_driver()

        logging.info(f"Initialized {self.pool} on {self.pool.system_name()}")
        logging.info(f"Download path: '{self.pool.download_path}'")

    def run_loop(self):
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

    def single_page_download(self, number=0):
        tracks = self.pool.download_page(number)
        logging.info(f"Page {self.pool.current_num}: downloaded {tracks} files.")

    def single_page_loop(self):
        self.pool.update_current_page()
        while True:
            print_bold(f"--- Page: {self.pool.current_num} ---")
            try:
                number = int(input("Give number of tracks to download from current page, 0 = all\n"))
                number = max(0, number)
            except ValueError:
                number = 0

            self.single_page_download(number)
            if not self.pool.next_page():
                print_color("No more pages!", Color.red)
                break

            self.play_notification_sound()
            if not input("Continue?\n").lower() in ("y", "1"):
                break

    def multi_page_loop(self, pages=1):
        self.pool.update_current_page()
        last_page = self.pool.current_num + pages - 1
        for _ in range(1, pages + 1):
            print_bold(f"--- Page: {self.pool.current_num} / {last_page} ---")
            self.single_page_download()
            if not self.pool.next_page():
                print_color("No more pages!", Color.red)
                return

        print_bold("Continue for pages?")
        self.play_notification_sound()
        try:
            num = int(input())
            if num > 0:
                self.multi_page_loop(num)
        except ValueError:
            return

    def play_notification_sound(self):
        """Play system notification sound without waiting for function call to finish."""
        threading.Thread(target=self._play_notification, args=(self.pool.mac_os(),)).start()

    @staticmethod
    def _play_notification(mac: bool):
        if mac:
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        else:
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)


def main(args):
    print_bold("/////// RECORDPOOL AUTO-DL ///////", Color.green)
    site = None if not args else args[0].lower()
    while not site:
        print_bold("\nChoose record pool:")
        options = dict(zip(("1", "2", "3", "4"), ("Beatjunkies", "DJCity", "BPMSupreme", "Bandcamp")))
        for key, value in options.items():
            print(f"{key}: {value}")

        ans = input()
        if options.get(ans):
            site = options[ans].lower()
        else:
            print("Error. Give a valid option...")

    try:
        downloader = RecordPoolDownloader(site)
        if site == "bandcamp":
            downloader.pool.download_page()
            downloader.pool.open_page("chrome://downloads/")
            input("Wait until downloads have finished...\n")
        else:
            downloader.run_loop()

    except Exception:
        logging.exception("Exception raised!")
        error_type, error_value, trace = sys.exc_info()
        print_bold(f"Error: {error_type}", Color.red)
        print_color(str(error_value), Color.red)
        for line in traceback.format_tb(trace):
            print_color(line, Color.yellow)

        return 1


if __name__ == '__main__':
    main(sys.argv[1:])
