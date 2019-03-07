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
    end_tag = '-->'

    with open(file, 'r+') as f: 
        file_string = f.read()
        start_byte = file_string.find(start_tag)

        while(start_byte != -1):
            f.seek(0)        
            file_string = f.read()
            start_byte = file_string.find(start_tag)
            end_byte = file_string.find(end_tag) + start_byte + len(end_tag)
            
            f.seek(start_byte)
            found = f.read(end_byte - start_byte)

            file_string = "%s%s%s" % (
                file_string[:start_byte], found[len(start_tag):len(found)-len(end_tag)] , file_string[end_byte:])

            f.seek(0)
            f.write(file_string)
            start_byte = file_string.find(start_tag)
            end_byte = file_string.find(end_tag) + start_byte + len(end_tag)

def uncomment(comments):
    for datasheet in datasheet_list:
        for comment in comments:
            if glob.glob(os.path.dirname(datasheet)+'/*' + comment):
                comment_files = list(Path(os.path.dirname(datasheet)).rglob('*'+comment))
                for comment_file in comment_files:
                    parse_html(datasheet, comment)

datasheet_list = get_file_tree(path_to_files)
comments = ['.db']
uncomment(comments)

