import os
import shutil
import sys

from scraper import Scraper


def main(argv="https://www.cyfrowe.pl/aparaty.html"):
    if os.path.exists("csv"):
        shutil.rmtree("csv")

    if os.path.exists("photos"):
        shutil.rmtree("photos")

    os.makedirs("csv")
    os.makedirs("photos")

    scraper = Scraper()
    scraper.start(argv)


if __name__ == "__main__":
    main()
