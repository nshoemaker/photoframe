#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import sys

LOG_FILENAME = "/usr/local/log/photoframe.log"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Service for photoframe")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument('installDir', metavar='D', help='The directory where the python files are')

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

BASE_DIR = args.installDir + "/"

# Deafults
LOG_FILENAME = BASE_DIR + "photoframe.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"


PIC_LOCATION = BASE_DIR + "attachments"

sys.path.append(BASE_DIR + 'Email')
from AttachmentDownloader import AttachmentDownloader
from Credentials import Credentials
sys.path.append(BASE_DIR)
from slideshow import App

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

app = App(1500, PIC_LOCATION)
app.show_slides()
app.update_cycle()
app.run()

ad = AttachmentDownloader(Credentials.readFromFile("../credentials.txt"), 1, PIC_LOCATION, (app.winfo_screenwidth, app.winfo_screenheight))