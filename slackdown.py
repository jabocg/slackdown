#!/usr/bin/env python3
# -*- coding: <encoding name> -*-

"""
Slackdown -- The Slack to Markdown converter.
"""

from collections import namedtuple
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import sys
from time import strftime
from zipfile import ZipFile

temppath = '.tmp/'

User = namedtuple('User', ['username', 'fullname', 'userid'])

# logging setup
verbose = True if sys.argv[1] == '-v' else False
if not os.path.isdir('log'):
    if os.path.exists('log'):
        os.remove('log')
    os.mkdir('log')
logfile = 'log/{}.log'.format(strftime('%Y%m%dT%H%M%S'))
logfmt = '%(asctime)s - %(module)s - %(levelname)s - '
logfmt += '%(funcName)s(%(lineno)d) - %(message)s'
logging.basicConfig(filename=logfile,
                    format=logfmt, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if verbose else logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def main():
    extractRecords()
    users = getUsers()
    channels = [p for p in Path(temppath).iterdir() if p.is_dir()]
    for c in channels:
        channelName = c.name
        logger.debug('subdir: {}'.format(c))
        logger.info('converting channel #{}'.format(channelName))
        for f in list(c.glob('*.json')):
            jsonToMarkdown(f)
        concatFiles(channelName, list(c.glob('*.md')).sort())


def jsonToMarkdown(jsonFile):
    """Translate a JSON file to a markdown file.

    Parameters:
        jsonFile -- pathlib.Path object representing a file
    """
    logger.debug('jsonFile: {}'.format(jsonFile))
    mdFileName = jsonFile.parent / (jsonFile.stem + '.md')
    logger.debug('mdFile: {}'.format(mdFileName))
    with jsonFile.open() as f:
        messages = json.loads(f.read())
    logger.debug('json object: {}'.format(messages))
    with mdFileName.open(mode='w') as mdf:
        for m in messages:
            logger.debug('message data: {}'.format(m))
            message = m['text']
            userid = m['user']
            timestamp = datetime.fromtimestamp(int(m['ts'].split('.')[0]))
            mdf.write('{} - **{}**: {}\n\n'.format(timestamp, userid, message))


def concatFiles(filename, files):
    """Concatenate a list of files into one file.

    Parameters:
        fileName -- name of the ending file
        files -- list of files to concatenate
    """
    logger.debug('filename: {}'.format(filename))
    logger.debug('files: {}'.format(files))


def getUsers():
    """Get users and pertinent data.

    Returns:
        list -- list of named tuples containing User's ID, username, and Full 
                Name
    """
    users = []
    userFile = Path(temppath) / 'users.json'
    logger.debug('getting users from {}'.format(userFile))
    with userFile.open() as f:
        userdata = json.loads(f.read())
        logger.debug('got userdata: {}'.format(userdata))
        for u in userdata:
            logger.debug('creating user {}'.format(u))
            users.append(User(u['name'], u['real_name'], u['id']))
    logger.debug('full list of users: {}'.format(users))
    return users


def extractRecords():
    logger.debug('zip file: {}'.format(sys.argv[-1]))
    logger.debug('temp path: {}'.format(temppath))
    zfile = ZipFile(sys.argv[-1])
    zfile.extractall(path=temppath)


if __name__ == '__main__':
    main()
