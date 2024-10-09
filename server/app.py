from flask import Flask, send_from_directory, json, Response, request
from waitress import serve
from flask_cors import CORS, cross_origin
from model import SugoiTranslator


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('dist', "index.html")

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('.', filename)

@app.route('/assets/<path:filename>')
def download_assets(filename):
    return send_from_directory('dist/assets', filename)

@app.route('/api/translate', methods= ['POST'])
@cross_origin()
def translate_api(): 
    input_text = request.args.get('text')
    sugoiTranslator = SugoiTranslator()
    if isinstance(input_text, str) and len(input_text) > 0: 
        text = sugoiTranslator.translate(input_text)
        return json.dumps(text)
    return Response(status= 400)


if __name__ == '__main__':
    serve(app)


