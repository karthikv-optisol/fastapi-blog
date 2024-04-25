from fastapi import APIRouter
from fastapi import FastAPI, Response, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..database import engine, get_db

router = APIRouter()

models.Base.metadata.create_all(engine)

        
@router.get(
    "/blogs", status_code=200, response_model=List[schemas.showBlog], tags=["Blogs"]
)
def getAll(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/blogs", tags=["Blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.title == request.title).first()

    if blog:
        raise HTTPException(status_code=302, detail=f"Blod with the title {request.title} already exists")  # type: ignore
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=request.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blog/{id}", status_code=200, response_model=schemas.showBlog, tags=["Blogs"])
def getBlog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blod with the id {id} not found")  # type: ignore
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'Blod with the id {id} not found'}
    return blog

@router.put("/blog/{id}", status_code=202, tags=["Blogs"])
def updateBlog(
    id: int, request: schemas.Blog, response: Response, db: Session = Depends(get_db)
):

    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blod with the id {id} not found")  # type: ignore

    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Blog updated successfully"


@router.delete("/blog/{id}", tags=["Blogs"])
def deleteBlog(id: int, response: Response, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blod with the id {id} not found")  # type: ignore

    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted successfully"