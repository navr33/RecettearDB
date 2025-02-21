from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from fastapi import FastAPI, Depends, File, UploadFile
from database import Category, Usage, Location, Items, get_db, add_to_db, update_data, remove_from_db
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/category")
def get_category(db: Session = Depends(get_db)):
    """
    Endpoint to obtain all categories and their respective usage.
    """
    formatter = lambda x: {"name": x.name,
                           "usage": x.usage,}
    return list(map(lambda x: formatter(x), db.query(Category).all()))


@app.get("/usage")
def get_usage(db: Session = Depends(get_db)):
    """
    Endpoint to obtain all usage types.
    """
    return list(map(lambda x: {"usage": x.usage}, db.query(Usage).all()))


@app.get("/location")
def get_location(db: Session = Depends(get_db)):
    """
    Endpoint to obtain all location types.
    """
    return list(map(lambda x: {"location": x.name}, db.query(Location).all()))


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    """
    Endpoint to obtain all items in the database.
    """
    formatter = lambda x: {"name": x.name,
                           "category": x.category,
                           "price": x.price,
                           "effect": x.effect,
                           "location": x.location}
    return list(map(lambda x: formatter(x), db.query(Items).all()))


@app.post("/items")
def add_item(name: str, category: str, price: int, effect: str, location, db: Session = Depends(get_db)):
    """
    Endpoint to add an item to the database.
    """
    new_item = Items(name, category, price, effect, location)
    return add_to_db(new_item, db)


@app.put("/items")
def edit_item(name: str, category: str, price: int, effect: str, location, db: Session = Depends(get_db)):
    """
    Endpoint to make changes to an item already in the database.
    """
    target = db.query(Items).filter(Items.name == name)[0]
    new_item = Items(name, category, price, effect, location)
    return update_data(target, new_item, db)


@app.delete("/items")
def remove_item(name: str, db: Session = Depends(get_db)):
    """
    Endpoint remove an item from the database.
    """
    target = db.query(Items).filter(Items.name == name)[0]
    return remove_from_db(target, db)



