# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
import os
import glob
from pathlib import Path


# This is the path to the directory you would like to search
# This directory is searched recursively for .html files

path_to_files = sys.argv[1]


def get_file_tree(path):
    return list(Path(path).rglob("*.html"))


def parse_html(file, comment):
    start_tag = '<!--'+comment
    end_tag = comment+'-->'

    with open(file, 'r') as f:

        file_string = f.read()

    with open(file, 'w') as f:

        file_string = file_string.replace(start_tag,"")
        file_string = file_string.replace(end_tag,"")

        f.write(file_string)

def uncomment(comments):
    comment_files = []
    for datasheet in datasheet_list:
        for comment in comments:
            if glob.glob(os.path.dirname(datasheet)+'/*' + comment):
                   parse_html(datasheet, comment)

datasheet_list = get_file_tree(path_to_files)
comments = ['.db']
uncomment(comments)

