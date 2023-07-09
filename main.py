from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


# title str : content: str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello API"}


@app.get("/posts")
async def get_roots():
    return {"message": "My posts"}


@app.post("/createpost")
async def create_post(new_post: Post):
    print(new_post)
    return {
        f"title: {new_post.title}": f"content: {new_post.content}, \
            published: {new_post.published}"    
    }
