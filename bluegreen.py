import sys
import logging

from bluegreen import BlueGreen

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("starting...")
    bg=BlueGreen()
    bg.main()

