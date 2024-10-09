from flask import Flask, send_from_directory


app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('dist', "index.html")

@app.route('/assets/<path:filename>')
def download_file(filename):
    return send_from_directory('dist/assets', filename)

if __name__ == '__main__':
    app.run(debug=True)


