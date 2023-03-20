'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
import os, os.path
from backend import File_Handler
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def homePage():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the file from the request
        file = request.files['file']
        file = file.read()
        # Get the string from the request
        language = request.form['lang']
        type = request.form['request_type'] # Summary? or transcription?
        word_limit = request.form['word_limit']

        response = File_Handler(language=language, req_type=type, word_limit=word_limit, file=file)
        return response
    except Exception as e:
        return {'status': 'Error: %s' % str(e)}

@app.errorhandler(404)
def pageNotFound(error):
    return {'status': '404 Page Not Found'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')