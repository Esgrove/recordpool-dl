"""
Record Pool Downloader
Akseli Lukkarila
2019
"""
import sys
import traceback

from colorprint import Color, print_bold, print_color

from Beatjunkies import Beatjunkies
from BPMSupreme import BPMSupreme
from DJCity import DJCity
from Bandcamp import Bandcamp


class RecordPoolDownloader:
    """ Command line tool for recordpool web downloads."""
    def __init__(self, site):
        if site.lower() == "beatjunkies":
            self.pool = Beatjunkies()
        elif site.lower() == "bpmsupreme":
            self.pool = BPMSupreme()
        elif site.lower() == "djcity":
            self.pool = DJCity()
        elif site.lower() == "bandcamp":
            self.pool = Bandcamp()
        else:
            raise RuntimeError("Unsupported record pool!")

        self.pool.start_driver()

    def run_loop(self):
        print_bold("\nChoose mode:")
        print(" 0: Single page")
        print(">0: Multipage with given number of pages")
        try:
            number = int(input())
            print()
            if number:
                self.multi_page_loop(number)
            else:
                self.single_page_loop()

        except ValueError:
            self.single_page_loop()

    def single_page_loop(self):
        self.pool.update_current_page()
        while True:
            print_bold(f"--- Page: {self.pool.current_num} ---")
            try:
                number = int(input("Give number of tracks to download from current page, 0 = all\n"))
                number = max(0, number)
            except ValueError:
                number = 0

            self.pool.download_page(number)
            if not input("Continue?\n").lower() in ("y", "1"):
                break

            if not self.pool.next_page():
                print_color("No more pages!", Color.red)
                break

    def multi_page_loop(self, pages=1):
        self.pool.update_current_page()
        last_page = self.pool.current_num + pages - 1
        for _ in range(1, pages + 1):
            print_bold(f"--- Page: {self.pool.current_num} / {last_page} ---")
            self.pool.download_page()
            if not self.pool.next_page():
                return

        print_bold("Continue for pages?")
        try:
            num = int(input())
            self.multi_page_loop(num)

        except ValueError:
            return


def main(args):
    print_bold("/////// RECORDPOOL AUTO-DL ///////", Color.green)

    site = None if not args else args[0]
    while not site:
        print_bold("\nChoose record pool:")
        for index, name in enumerate(("Beatjunkies", "DJCity", "BPM Supreme", "Bandcamp"), 1):
            print(f"{index}: {name}")

        ans = input()
        if ans.lower() in ("1", "b"):
            site = "beatjunkies"
        elif ans.lower() in ("2", "d"):
            site = "djcity"
        elif ans.lower() in ("3", "s"):
            site = "bpmsupreme"
        elif ans.lower() in ("4", "c"):
            site = "bandcamp"
        else:
            print("Error. Give a correct answer...")

    try:
        downloader = RecordPoolDownloader(site)
        if site == "bandcamp":
            downloader.pool.download_page()
            downloader.pool.open_page("chrome://downloads/")
            input("Wait until downloads have finished...\n")
        else:
            downloader.run_loop()

    except Exception:
        error_type, error_value, trace = sys.exc_info()
        print_bold(f"Error: {error_type}", Color.red)
        print_color(str(error_value), Color.red)
        for line in traceback.format_tb(trace):
            print_color(line, Color.yellow)

        return 1


if __name__ == '__main__':
    main(sys.argv[1:])
