from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends

Base = declarative_base()
engine = create_engine("sqlite+pysqlite:///recettear_items.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

# Definicion de Clases

class Category(Base):
    __tablename__ = "category"

    name = Column(String, primary_key=True)
    usage = Column (String)

    def __init__(self, name, usage):
        self.name = name
        self.usage = usage


class Usage(Base):
    __tablename__ = "usage"

    usage = Column(String, primary_key=True)

    def __init__(self, usage):
        self.usage = usage


class Location(Base):
    __tablename__ = "location"

    name = Column(String, primary_key=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Items(Base):
    __tablename__ = "items"

    name = Column(String, primary_key=True, nullable=False)
    category = Column(String, ForeignKey(Category.name), nullable=False)
    price = Column(Integer)
    effect = Column(String)
    location = Column(String, ForeignKey(Location.name))

    def __init__(self, name, category, price, effect, location):
        self.name = name
        self.category = category
        self.price = price
        self.effect = effect
        self.location = location



# Interaccion con base de datos
        
def get_db():
    """
    Retorna un objeto de sesión SQLAlchemy para interactuar con la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_to_db(data, session):
    """
    Agrega un objeto a la base de datos.
    """
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
    except IntegrityError as e:
        session.rollback()
        return 'Error al agregar'
    except Exception as e:
        session.rollback()
        return 'Error desconocido'
    return 'Aceptado'

def remove_from_db(data, session):
    """
    Elimina un objeto de la base de datos
    """
    try:
        session.delete(data)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        return 'Error al eliminar'
    except Exception as e:
        session.rollback()
        return 'Error desconocido'
    return 'Aceptado'

def update_data(old_data, new_data, session):
    """
    Reemplaza un objeto en la base de datos.
    """
    session.delete(old_data)
    session.commit()
    try:
        session.add(new_data)
        session.commit()
        session.refresh(new_data)
    except IntegrityError as e:
        session.rollback()
        session.add(old_data)
        session.commit()
        session.refresh(old_data)
        return 'Error al actualizar'
    except Exception as e:
        session.rollback()
        session.add(old_data)
        session.commit()
        session.refresh(old_data)
        return 'Error desconocido'
    return 'Aceptado'

