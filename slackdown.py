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


def readChannel():
    pass


if __name__ == '__main__':
    __main__()
