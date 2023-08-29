from fastapi import FastAPI
import uvicorn

from uce.ai.openuce import Document, process_inference

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/inference")
def inference(doc: Document):
    ingredientes = process_inference(doc.item)
    return {
        'response': ingredientes
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port='2588')