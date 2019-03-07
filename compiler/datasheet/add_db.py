from pathlib import Path
import glob
import os

# This is the path to the directory you would like to search
# This directory is searched recursively for .html files

path_to_files = '../temp/'


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

