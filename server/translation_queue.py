import redis, time, logging, sys, json
from model import SugoiTranslator
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


