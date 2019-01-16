import library
from pathlib import Path


class library_item():
    def __init__(self):
        self.name = ''
        self.comment = ''
        self.word_size = ''
        self.num_words = ''
        self.num_banks = ''
        self.num_rw_ports = ''
        self.num_r_ports = ''
        self.num_w_ports = ''
        self.Area = ''
        self.git_id = ''
        self.tech_name = ''
        self.min_period = ''
        self.datetime = ''


class library_gen():
    def library_write(name, book):
        with open(name, 'w+') as f:
            library_page.generate_html(book)
            f.write(library_page.html)

    def search_file(file, name):
        length = len(name)
        part = file.read(length)
        i = 0
        while True:
            if part == name:
                break
            char = file.read(1)
            if not char:
                return
            part = part[1:] + char
            i += 1
        return i

    def parse_comment(item):
        row = item.comment.split(',')
        print(row)
        found = 0
        col = 0

        item.name = row[col]
        col += 1

        item.num_words = row[col]
        col += 1

        item.num_banks = row[col]
        col += 1

        item.num_rw_ports = row[col]
        col += 1

        item.num_w_port = row[col]
        col += 1

        item.num_r_ports = row[col]
        col += 1

        item.tech_name = row[col]
        col += 1
        print(item.tech_name)
#        TEMP = row[col]
        col += 1

#        VOLT = row[col]
        col += 1

#        PROC = row[col]
        col += 1

        item.min_period = row[col]
        col += 1
        print(item.min_period)
#        OUT_DIR = row[col]
        col += 1

#        LIB_NAME = row[col]
        col += 1

        item.word_size = row[col]
        col += 1

        item.git_id = row[col]
        col += 1

        item.datetime = row[col]
        col += 1

#        DRC = row[col]
        col += 1

#        LVS = row[col]
        col += 1

    def parse_html(file):
        item = library_item()
        start_tag = '<!--'
        end_tag = '-->'

        with open(file, 'r') as f:
            start_byte = library_gen.search_file(f, start_tag) + len(start_tag)
            end_byte = library_gen.search_file(f, end_tag) + start_byte

            f.seek(start_byte)
            item.comment = f.read(end_byte - start_byte)
        library_gen.parse_comment(item)

        return item

    def get_file_tree(path):
        return list(Path(path).rglob("*.html"))


datasheet_list = library_gen.get_file_tree('./deliverables')
print(datasheet_list)
library_page = library.library()
book = []
for datasheet in datasheet_list:
    book.append(library_gen.parse_html(datasheet))
library_gen.library_write('index.html', book)
