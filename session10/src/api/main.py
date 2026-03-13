import json
import requests
from fastapi import FastAPI

OLLAMA_MODEL = "smollm:135m-base-v0.2-q2_K"

api = FastAPI()

@api.post("/chat")
def chat(message: str):
    # request ollama without streaming
    response = requests.post("http://ollama:11434/api/generate", json={"model": OLLAMA_MODEL, "prompt": message})
    result = []
    for line in response.iter_lines():
        line = json.loads(line)
        if line and 'response' in line:
            result.append(line['response'])

    return {"response": "".join(result)}