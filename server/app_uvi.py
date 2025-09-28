import uuid, json, ast
from threading import Thread
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from translation_queue import query_translation, queue_process, queue_key, redis_client, logging
from typing import List



app = FastAPI()
DIST_DIR = Path("dist")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequestBody(BaseModel):
    input_texts: List[str]

app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")
app.mount("/public", StaticFiles(directory=DIST_DIR / "public"), name="public")
#app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="spa")


@app.get("/")
async def home():
    return FileResponse(DIST_DIR / "index.html")

@app.get('/api/translate')
async def translate_get(text: str):
    input_text = text
    if isinstance(input_text, str) and len(input_text) > 0: 
        task_id = str(uuid.uuid4())
        redis_client.lpush(queue_key, json.dumps({
            "id": task_id,
            "input": input_text
        })) # left push
        result = query_translation(task_id)
        if result is not None: return { "text": result }
        else: return JSONResponse(status_code= 529, content={"error": "Server overloaded"})
    return Response(status_code= 400)

@app.post('/api/translate')
async def translate_post(request_body: PostRequestBody):
    if isinstance(request_body.input_texts, list) and len(request_body.input_texts):
        task_id = str(uuid.uuid4())
        redis_client.lpush(queue_key, json.dumps({
            "id": task_id,
            "input": request_body.input_texts
        })) # left push
        result = query_translation(task_id)
        if result is not None: return { "translations": ast.literal_eval(result) }
        else: return JSONResponse(status_code= 529, content={"error": "Server overloaded"})
    return Response(status_code= 400)



if __name__ == '__main__':
    Thread(target=queue_process, daemon=True).start()
    logging.info("Starting server...")
    try: uvicorn.run("app_uvi:app", host="0.0.0.0", port=7860, reload=True)
    except BaseException as e: 
        logging.info(e)


