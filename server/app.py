from threading import Thread
import redis, time
from flask import Flask, send_from_directory, json, Response, request
from waitress import serve
from flask_cors import CORS, cross_origin
from model import SugoiTranslator
from typing import List


queue_key = "translation_queue"
translated_key = "translated_temp_store"
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def queue_process():
    while True:
        task_list = []
        for _ in range(5):
            task = redis_client.rpop(queue_key) # right pop
            if task: task_list.append(task)
            else: break

        if len(task_list): task_process(task_list)

def task_process(input_text_list: List[str]):
    sugoiTranslator = SugoiTranslator()
    translations = sugoiTranslator.translate(input_text_list)
    for index, translation in enumerate(translations): 
        redis_client.hset(translated_key, input_text_list[index], translation)

def query_translation(input_text: str):
    for _ in range(30):
        translated_text = redis_client.hget(translated_key, input_text)
        if translated_text: 
            redis_client.hdel(translated_key, input_text)
            return translated_text
        time.sleep(1)




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
    if isinstance(input_text, str) and len(input_text) > 0: 
        redis_client.lpush(queue_key, input_text) # left push
        result = query_translation(input_text)
        if result is not None: return json.dumps({ "text": str(result) })
        else: Response(status= 500)
    return Response(status= 400)


if __name__ == '__main__':
    Thread(target=queue_process, daemon=True).start()
    print("Starting server...")
    try: serve(app, port= 7860)
    except: serve(app, port= 7860)


