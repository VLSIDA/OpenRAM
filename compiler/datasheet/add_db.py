from pathlib import Path
import glob
import os

# This is the path to the directory you would like to search
# This directory is searched recursively for .html files

path_to_files = '../temp/'


def get_file_tree(path):
    return list(Path(path).rglob("*.html"))


def parse_html(file, db):
    start_tag = 'Deliverables</p><table id= "data"><thead><tr><th>Type</th><th>Description</th><th>Link</th></tr></thead><tbody><tr><tr>'
    with open(file, 'r+') as f:

        file_string = f.read()
        start_byte = file_string.find(start_tag) + len(start_tag)
        row = '<tr><td>.db</td><td>Compiled .lib file</td><td><a href="' + \
            str(db)+'">'+str(os.path.basename(db))+'</a></td></tr>'
        file_string = "%s%s%s" % (
            file_string[:start_byte], row, file_string[start_byte:])
        f.seek(0)
        f.write(file_string)


datasheet_list = get_file_tree(path_to_files)
for datasheet in datasheet_list:
    if glob.glob(os.path.dirname(datasheet)+'/*.db'):
        db_files = list(Path(os.path.dirname(datasheet)).rglob("*.db"))
        for db_file in db_files:
            parse_html(datasheet, db_file)
