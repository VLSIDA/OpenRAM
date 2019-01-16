import os
import base64


class library():

    def __init__(self):
        self.html = ''

    def generate_html(self):
        vlsi_logo = 0
        with open(os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/datasheet/assets/vlsi_logo.png', "rb") as image_file:
            vlsi_logo = base64.b64encode(image_file.read())

        self.html += '<a href="https://vlsida.soe.ucsc.edu/"><img src="data:image/png;base64,{0}" alt="VLSIDA"></a>'.format(str(vlsi_logo)[
                                                                                                                            2:-1])
