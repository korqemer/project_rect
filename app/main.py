from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


# title str : content: str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
   
    cursor = conn.cursor()
    print("Connection succesful")
     
except Exception as error:
    print("Error")
    print(error)


@app.get("/")
async def root():
    return {"message": "Hello API"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    message = cursor.fetchone()
    conn.commit()
    return {
        "state": message
    }


@app.get("/posts/{id}")
def get_post(id: str, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id), ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ID not found")
    return {"id": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cursor.execute("DELETE from posts where id = %s returning *", (str(id), ))
    post = cursor.fetchone()
    if post:
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO ID")


@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    cursor.execute('''update posts set title=%s, content=%s, published=%s
                   where id=%s
                   returning *''',
                   ( post.title, post.content, post.published, str(id),))
    post = cursor.fetchone()
    if (post is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NO ID")
    conn.commit()
    return {"data": post}
