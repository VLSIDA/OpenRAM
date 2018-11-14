import os
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        dirname = os.path.dirname(os.path.abspath(__file__))
        f.save(dirname + '/uploads/' +  secure_filename(f.filename))
        return 'file uploaded successfully'
	
if __name__ == '__main__':
    app.run(debug = True)
