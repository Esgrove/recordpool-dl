"""
Record Pool Downloader
Akseli Lukkarila
2019
"""
import sys
import traceback

import colorama

from colorprint import Color, printBold, printColor
from Beatjunkies import Beatjunkies
from BPMSupreme import BPMSupreme
from DJCity import DJCity


class RecordPoolDownloader:
    """ Command line tool for recordpool web downloads."""
    def __init__(self, site):
        if site.lower() == "beatjunkies":
            self.pool = Beatjunkies()

        elif site.lower() == "bpmsupreme":
            self.pool = BPMSupreme()

        elif site.lower() == "djcity":
            self.pool = DJCity()

        else:
            raise RuntimeError("Unsupported record pool!")

        self.pool.start_driver()

    def run_loop(self):
        printBold("\nChoose mode:")
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
            printBold(f"--- Page: {self.pool.current_num} ---")
            try:
                number = int(input("Give number of tracks to download from current page, 0 = all\n"))
                number = max(0, number)
            except ValueError:
                number = 0

            self.pool.download_page(number)
            if not input("Continue?\n").lower() in ("y", "1"):
                break

            if not self.pool.next_page():
                printColor("No more pages!", Color.red)
                break

    def multi_page_loop(self, pages=1):
        self.pool.update_current_page()
        last_page = self.pool.current_num + pages - 1
        for _ in range(1, pages + 1):
            printBold(f"--- Page: {self.pool.current_num} / {last_page} ---")
            self.pool.download_page()
            if not self.pool.next_page():
                return

        printBold("Continue for pages?")
        try:
            num = int(input())
            self.multi_page_loop(num)

        except ValueError:
            return


def main():
    colorama.init()
    printBold("/////// RECORDPOOL AUTO-DL ///////", Color.green)

    site = None if len(sys.argv) < 2 else sys.argv[1]
    while not site:
        printBold("\nChoose record pool:")
        for index, name in enumerate(("Beatjunkies", "DJCity", "BPM Supreme"), 1):
            print(f"{index}: {name}")

        ans = input()
        if ans.lower() in ("1", "b"):
            site = "beatjunkies"
        elif ans.lower() in ("2", "d"):
            site = "djcity"
        elif ans.lower() in ("3", "s"):
            site = "bpmsupreme"
        else:
            print("Error. Give a correct answer...")

    try:
        downloader = RecordPoolDownloader(site)
        downloader.run_loop()
    except Exception:
        error_type, error_value, trace = sys.exc_info()
        printBold(f"Error: {error_type}", Color.red)
        printColor(str(error_value), Color.red)
        for line in traceback.format_tb(trace):
            printColor(line, Color.yellow)

        return 1


if __name__ == '__main__':
    main()
