import os
import shutil
import sys

from scraper import Scraper


def main(argv):
    if os.path.exists("csv"):
        shutil.rmtree("csv")

    if os.path.exists("photos"):
        shutil.rmtree("photos")

    os.makedirs("csv")
    os.makedirs("photos")

    scraper = Scraper()
    scraper.start(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
