from fastapi import APIRouter
from fastapi import FastAPI, Response, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..database import engine, get_db
from passlib.context import CryptContext

router = APIRouter()

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/user/register", tags=["Users"])
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        raise HTTPException(status_code=302, detail=f"User with the email {request.email} already exists")  # type: ignore

    password = get_password_hash(request.password)

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=password,
        gender=request.gender,
        mobile=request.mobile,
        isOnline=request.isOnline,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/users/login", tags=["Users"])
def login(request: schemas.loginUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=302, detail=f"User with the email {request.email} not exists")  # type: ignore

    password = verify_password(request.password, user.password)

    if not password:
        raise HTTPException(status_code=302, detail=f"The password you entered not matched")  # type: ignore

    return {"data": "User loggedIn succesfully"}


@router.get(
    "/users", status_code=200, response_model=List[schemas.showUser], tags=["Users"]
)
def getAll(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get(
    "/users/{id}", status_code=200, response_model=schemas.showUser, tags=["Users"]
)
def getUsers(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
