#!/usr/bin/env python3
# -*- coding: <encoding name> -*-

"""
Slackdown -- The Slack to Markdown converter.
"""

import logging
import os
from pathlib import Path
import sys
from time import strftime
import zipfile

temppath = '.tmp/'

# logging setup
if not os.path.isdir('log'):
    if os.path.exists('log'):
        os.remove('log')
    os.mkdir('log')
logfile = 'log/{}.log'.format(strftime('%Y%m%dT%H%M%S'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logfmt = '%(asctime)s - %(module)s - %(levelname)s - '
logfmt += '%(funcName)s(%(lineno)d) - %(message)s'
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format=logfmt, datefmt='%Y-%m-%d %H:%M:%S')


def __main__():
    extractRecords()
    channels = [p for p in Path(temppath).iterdir() if p.is_dir()]
    for c in channels:
        cname = c.parts[-1]
        logger.debug('channel name: {}'.format(cname))
        logger.debug('subdir: {}'.format(c))
        for f in list(c.glob('*.json')):
            jsonToMarkdown(f)


def jsonToMarkdown(jsonFile):
    """Translate a JSON file to a markdown file.

    Parameters:
        jsonFile -- pathlib.Path object representing a file
    """
    pass


def extractRecords():
    zfile = zipfile.ZipFile(sys.argv[1])
    zfile.extractall(path=temppath)


if __name__ == '__main__':
    __main__()
