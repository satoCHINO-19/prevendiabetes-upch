from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Encuesta(Base):
    __tablename__ = "encuestas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    edad = Column(Integer)
    genero = Column(String)
    universidad = Column(String, default="UPCH")
    facultad = Column(String, nullable=True)
    
    # Respuestas 1-24
    p1 = Column(Integer)
    p2 = Column(Integer)
    p3 = Column(Integer)
    p4 = Column(Integer)
    p5 = Column(Integer)
    p6 = Column(Integer)
    p7 = Column(Integer)
    p8 = Column(Integer)
    p9 = Column(Integer)
    p10 = Column(Integer)
    p11 = Column(Integer)
    p12 = Column(Integer)
    p13 = Column(Integer)
    p14 = Column(Integer)
    p15 = Column(Integer)
    p16 = Column(Integer)
    p17 = Column(Integer)
    p18 = Column(Integer)
    p19 = Column(Integer)
    p20 = Column(Integer)
    p21 = Column(Integer)
    p22 = Column(Integer)
    p23 = Column(Integer)
    p24 = Column(Integer)
    
    # Métricas calculadas
    puntaje_total = Column(Integer)
    puntaje_conocimiento = Column(Float)
    puntaje_alimentacion = Column(Float)
    puntaje_actividad = Column(Float)
    puntaje_antecedentes = Column(Float)
    puntaje_estres = Column(Float)
    puntaje_prevencion = Column(Float)
    categoria_riesgo = Column(String)
    
    fecha = Column(DateTime, default=datetime.utcnow)
