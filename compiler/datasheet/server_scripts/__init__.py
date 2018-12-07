import os
import jinja2
from flask import Flask, render_template
from filelist import *


filedir = './files'
file_data = './filelist.info'


app = Flask('server_scripts')


if __name__ == '__main__':
    
    files = filelist()

    files.update_filelist(filedir,file_data)
    
    f = open('./index.html','w')
    with app.app_context():
        f.write(render_template('index.html', filedir = filedir , os = os))

       
