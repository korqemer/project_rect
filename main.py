from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# title str : content: str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "foods", "content": "i like piazza", "id": 1},
            { "places" :" I like Kok Tobe", "content": "in almaty", "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello API"}


@app.get("/posts")
async def get_roots():
    return {"message": my_posts}


@app.post("/posts")
async def create_post(new_post: Post):
    return {
        "title": new_post
    }
