from threading import Thread
import redis, time, logging, sys, ast
from flask import Flask, jsonify, send_from_directory, Response, request
from waitress import serve
from flask_cors import CORS, cross_origin
from model import SugoiTranslator
import uuid, json
from typing import List, Dict, Any, Union



queue_key = "translation_queue"
translated_key = "translated_temp_store"
redis_client = redis.Redis(host='localhost', port=6379, db=0)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

def queue_process():
    while True:
        task_list = []
        for _ in range(5):
            json_string = redis_client.rpop(queue_key) # right pop
            if isinstance(json_string, (bytes, bytearray)):
                task: Dict[str, Any] = json.loads(json_string.decode("utf-8"))
                if isinstance(task["input"], list): task_process([ task ])
                elif isinstance(task["input"], str): task_list.append(task)
                elif task is not None: logging.info(task)
            elif json_string is not None: logging.info(json_string)

        if len(task_list): task_process(task_list)
        time.sleep(0.2)

def task_process(task: List[Dict[str, Any]]):
    logging.info(f"translating: {task}")
    input_text_list: List[str] = (
        task[0]["input"] if len(task)==1 and isinstance(task[0]["input"], list) 
        else list(map(lambda item: item["input"], task))
    )
    sugoiTranslator = SugoiTranslator()
    translations = sugoiTranslator.translate(input_text_list)
    if len(task)==1 and isinstance(task[0]["input"], list):
        return redis_client.hset(translated_key, task[0]["id"], str(translations))
    for index, translation in enumerate(translations): 
        redis_client.hset(translated_key, task[index]["id"], translation)

def query_translation(key: str) -> Union[str, None]:
    for _ in range(30):
        translated_text = redis_client.hget(translated_key, key)
        if translated_text is not None: 
            redis_client.hdel(translated_key, key)
            try: return translated_text.decode('utf-8')
            except AttributeError: return translated_text
        time.sleep(1)




app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('dist', "index.html")

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('dist', filename)

@app.route('/assets/<path:filename>')
def download_assets(filename):
    return send_from_directory('dist/assets', filename)

@app.route('/api/translate', methods= ["GET"])
@cross_origin()
def translate_get(): 
    input_text = request.args.get('text')
    if isinstance(input_text, str) and len(input_text) > 0: 
        task_id = str(uuid.uuid4())
        redis_client.lpush(queue_key, json.dumps({
            "id": task_id,
            "input": input_text
        })) # left push
        result = query_translation(task_id)
        if result is not None: return jsonify({ "text": result })
        else: return Response(status= 529, response= "Error 529: Server overloaded")
    return Response(status= 400)

@app.route('/api/translate', methods= ["POST"])
@cross_origin()
def translate_post():
    input_texts = request.get_json().get("input_texts")
    if isinstance(input_texts, list) and len(input_texts):
        task_id = str(uuid.uuid4())
        redis_client.lpush(queue_key, json.dumps({
            "id": task_id,
            "input": input_texts
        })) # left push
        result = query_translation(task_id)
        if result is not None: return jsonify({ "translations": ast.literal_eval(result) })
        else: return Response(status= 529, response= "Error 529: Server overloaded")
    return Response(status= 400)


if __name__ == '__main__':
    Thread(target=queue_process, daemon=True).start()
    logging.info("Starting server...")
    try: serve(app, port= 7860)
    except BaseException as e: 
        logging.info(e)


