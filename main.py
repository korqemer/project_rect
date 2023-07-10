from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


# title str : content: str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "foods", "content": "i like piazza", "id": 1},
            {"places": " I like Kok Tobe", "content": "in almaty", "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello API"}


@app.get("/posts")
async def get_roots():
    return {"message": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(10000000)
    my_posts.append(post_dict)
    return {
        "title": post_dict
    }


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return {"id": post}


def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    index = find_index(int(id))
    if index:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO ID")


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index(int(id))
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO ID")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
