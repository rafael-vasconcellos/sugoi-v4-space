from flask import Flask, send_from_directory
from waitress import serve
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('dist', "index.html")

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('.', filename)

@app.route('/assets/<path:filename>')
def download_file(filename):
    return send_from_directory('dist/assets', filename)

if __name__ == '__main__':
    serve(app)


