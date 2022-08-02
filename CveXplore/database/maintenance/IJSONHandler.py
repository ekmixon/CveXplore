import logging

import ijson

from .LogHandler import UpdateHandler

logging.setLoggerClass(UpdateHandler)


class IJSONHandler(object):
    def __init__(self):
        self.logger = logging.getLogger("IJSONHandler")

    def fetch(self, filename, prefix):
        x = 0
        with open(filename, "rb") as input_file:
            for item in ijson.items(input_file, prefix):
                yield item
                x += 1

        self.logger.debug(
            f"Processed {x} items from file: {filename}, using prefix: {prefix}"
        )
