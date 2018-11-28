import os
import jinja2
from flask import Flask, render_template
from filelist import *


filedir = './files'
file_data = './filelist.info'

def render_without_request(template_name, **template_vars):
    env = jinja2.Environment(
            loader = jinja2.PackageLoader('server_scripts','templates')
    )
    template = env.get_template(template_name)
    return template.render(**template_vars)

app = Flask('server_scripts')

if __name__ == '__main__':
    
    files = filelist()

    files.update_filelist(filedir,file_data)
    
    f = open('./output/index.html','w')
    with app.app_context():
        f.write(render_template('index.html', files=files.list))

       
