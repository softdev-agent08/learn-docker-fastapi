from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def aiquest():
    return {"message": "Hello World"}