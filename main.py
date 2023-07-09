from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello API"}

@app.get("/posts")
async def get_roots():
    return {"message": "My posts"}