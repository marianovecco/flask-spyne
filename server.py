from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, UnsignedInteger32
from spyne.model.complex import Iterable
from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

engine = create_engine('sqlite:///materias.db')

Base = declarative_base()

session = sessionmaker()
session.configure(bind=engine)

class Materia(Base):
    __tablename__ = 'materia'
    id = Column(Integer, primary_key=True)
    legajo = Column(Integer)
    name = Column(String)
    cuat = Column(String)
    nota = Column(Integer)

app = Flask(__name__)
spyne = Spyne(app)

class SomeSoapService(spyne.Service):
    __service_url_path__ = '/soap/someservice'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, _returns=Iterable(Unicode))
    def obtenerMateriaAlumno(legajo):
        materias = session.query(Materia).filter(Materia.legajo == legajo).all()
        for materia in materias:
            yield str(materia.name)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    session = session()

    materia = Materia(legajo=1234,name='matematica',cuat='1ero 2017',nota=10)
    session.add(materia)

    materia2 = Materia(legajo=1234,name='fisica',cuat='1ero 2017',nota=10)
    session.add(materia2)

    materia3= Materia(legajo=5678,name='quimica',cuat='2do 2017',nota=10)
    session.add(materia3)

    session.commit()
    app.run(host = '127.0.0.1')
