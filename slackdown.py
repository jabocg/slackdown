#!/usr/bin/env python3
# -*- coding: <encoding name> -*-

"""
Slackdown -- The Slack to Markdown converter.
"""

import zipfile
import sys


def __main__():
    print(sys.argv)
    zfile = zipfile.ZipFile(sys.argv[1])
    zfile.extractall(path='.tmp/')


def readChannel():
    pass


if __name__ == '__main__':
    __main__()
