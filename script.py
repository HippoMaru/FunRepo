import argparse
import logging
import os
from collections import namedtuple

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='absolute path to file')
args = parser.parse_args()

logging.basicConfig(filename="log.log", encoding="utf8", level=logging.INFO)
logger = logging.getLogger("log")

FILE = namedtuple("FILE", "name extension flag parent_directory")


def parse_dir(path):
    if not os.path.isdir(path):
        logger.error("wrong path to directory")
        return
    directory = os.fsencode(path)
    parent_directory = os.fsdecode(directory).split("\\")[-1]
    for file in os.listdir(directory):
        name, *extension = os.fsdecode(file).split(".")
        flag = "file" if extension else "directory"
        logger.info(
            FILE(name,
                 extension[0] if extension else None,
                 flag,
                 parent_directory)
        )
        if flag == "directory":
            temp_path = path + "\\" + name
            try:
                parse_dir(temp_path)
            except Exception:
                logger.warning("access denied: " + temp_path)


try:
    parse_dir(args.path)
except Exception:
    logger.warning("access denied: " + args.path)
