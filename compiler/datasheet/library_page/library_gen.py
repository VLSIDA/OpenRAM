import library
import csv


class library_item():
    def __init__(self):
        self.comment = ''
        self.word_size = ''
        self.num_words = ''
        self.num_banks = ''
        self.num_rw_ports = ''
        self.num_r_ports = ''
        self.num_w_ports = ''
        self.Area = ''
        self.git_id = ''
        self.technology = ''
        self.min_op = ''


class library_gen():
    def library_write(name):
        with open(name, 'w+') as f:
            library_page.generate_html()
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

    def parse_html(file):
        item = library_item()
        start_tag = '<!--'
        end_tag = '-->'

        with open(file, 'r') as f:
            start_byte = library_gen.search_file(f, start_tag) + len(start_tag)
            end_byte = library_gen.search_file(f, end_tag) + start_byte

            f.seek(start_byte)
            item.comment = f.read(end_byte - start_byte)
        print(item.comment)
        return item

    def parse_comment(comment, item):

        pass


library_page = library.library()
library_gen.parse_html('../../temp/sram_2_16_scn4m_subm.html')
