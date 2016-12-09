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
from zipfile import ZipFile

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


def main():
    extractRecords()
    channels = [p for p in Path(temppath).iterdir() if p.is_dir()]
    for c in channels:
        cname = c.name
        logger.debug('subdir: {}'.format(c))
        logger.info('converting channel #{}'.format(cname))
        for f in list(c.glob('*.json')):
            jsonToMarkdown(f)
        concatFiles(cname, list(c.glob('*.md')).sort())


def jsonToMarkdown(jsonFile):
    """Translate a JSON file to a markdown file.

    Parameters:
        jsonFile -- pathlib.Path object representing a file
    """
    logger.debug('jsonFile: {}'.format(jsonFile))
    mdFileName = jsonFile.parent / (jsonFile.stem + '.md')
    logger.debug('mdFile: {}'.format(mdFileName))


def concatFiles(filename, files):
    """Concatenate a list of files into one file.

    Parameters:
        fileName -- name of the ending file
        files -- list of files to concatenate
    """
    logger.debug('filename: {}'.format(filename))
    logger.debug('files: {}'.format(files))


def extractRecords():
    logger.debug('zip file: {}'.format(sys.argv[1]))
    logger.debug('temp path: {}'.format(temppath))
    zfile = ZipFile(sys.argv[1])
    zfile.extractall(path=temppath)


if __name__ == '__main__':
    main()
