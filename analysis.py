import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def analizar_tendencias(edad, genero, facultad, respuestas, db: Session):
    """Analiza tendencias personalizadas comparando con población similar"""
    
    # Obtener población similar
    query = db.query(models.Encuesta).filter(
        models.Encuesta.edad.between(edad - 3, edad + 3)
    )
    
    if genero in ["M", "F"]:
        query = query.filter(models.Encuesta.genero == genero)
    
    poblacion = pd.read_sql(query.statement, db.bind)
    
    if len(poblacion) < 10:
        poblacion = pd.read_sql(db.query(models.Encuesta).statement, db.bind)
    
    # Calcular percentiles
    puntaje_usuario = sum([respuestas[f"p{i}"] for i in range(1, 25)])
    percentil = (poblacion['puntaje_total'] < puntaje_usuario).sum() / len(poblacion) * 100
    
    # Identificar debilidades (dimensiones bajo percentil 40)
    dimensiones = {
        "Conocimiento": sum([respuestas[f"p{i}"] for i in range(1, 6)]),
        "Alimentación": sum([respuestas[f"p{i}"] for i in range(6, 11)]),
        "Actividad Física": sum([respuestas[f"p{i}"] for i in range(11, 15)]),
        "Control Personal": sum([respuestas[f"p{i}"] for i in range(15, 19)]),
        "Manejo del Estrés": sum([respuestas[f"p{i}"] for i in range(19, 22)]),
    }
    
    promedios = {
        "Conocimiento": poblacion[[f"p{i}" for i in range(1, 6)]].sum(axis=1).mean(),
        "Alimentación": poblacion[[f"p{i}" for i in range(6, 11)]].sum(axis=1).mean(),
        "Actividad Física": poblacion[[f"p{i}" for i in range(11, 15)]].sum(axis=1).mean(),
        "Control Personal": poblacion[[f"p{i}" for i in range(15, 19)]].sum(axis=1).mean(),
        "Manejo del Estrés": poblacion[[f"p{i}" for i in range(19, 22)]].sum(axis=1).mean(),
    }
    
    debilidades = [dim for dim, puntaje in dimensiones.items() 
                   if puntaje < promedios[dim] * 0.8]
    
    fortalezas = [dim for dim, puntaje in dimensiones.items() 
                  if puntaje > promedios[dim] * 1.1]
    
    # Comparación con facultad
    if facultad:
        fac_data = poblacion[poblacion['facultad'] == facultad]
        if len(fac_data) > 5:
            promedio_facultad = fac_data['puntaje_total'].mean()
            comparacion_fac = "mejor" if puntaje_usuario > promedio_facultad else "similar" if abs(puntaje_usuario - promedio_facultad) < 5 else "por debajo"
        else:
            comparacion_fac = "sin datos suficientes"
    else:
        comparacion_fac = "no especificada"
    
    return {
        "percentil": round(percentil, 1),
        "promedio_poblacion": round(poblacion['puntaje_total'].mean(), 1),
        "debilidades": debilidades,
        "fortalezas": fortalezas,
        "comparacion_facultad": comparacion_fac,
        "total_comparados": len(poblacion)
    }

def generar_recomendaciones(categoria, debilidades, percentil):
    """Genera recomendaciones personalizadas basadas en evidencia"""
    recomendaciones = []
    
    # Recomendaciones base según categoría
    if categoria == "Riesgo Alto":
        recomendaciones.append({
            "prioridad": "URGENTE",
            "accion": "Consulta médica preventiva",
            "detalle": "Solicita chequeo de glucosa en ayunas (≥100 mg/dL indica prediabetes). Referencia: INEI 2021 reporta 69.7% diagnósticos tardíos.",
            "plazo": "2 semanas"
        })
    
    # Recomendaciones por dimensión débil
    if "Alimentación" in debilidades:
        recomendaciones.append({
            "prioridad": "ALTA",
            "accion": "Plan nutricional DASH",
            "detalle": "Reduce azúcares añadidos 30%, aumenta fibra a 25-30g/día. Estudios demuestran reducción 58% riesgo DM2.",
            "plazo": "1 mes"
        })
    
    if "Actividad Física" in debilidades:
        recomendaciones.append({
            "prioridad": "ALTA",
            "accion": "Ejercicio aeróbico 150 min/semana",
            "detalle": "Caminar rápido 30 min/día, 5 días/semana reduce riesgo DM2 en 40% (OMS 2020).",
            "plazo": "Iniciar esta semana"
        })
    
    if "Manejo del Estrés" in debilidades:
        recomendaciones.append({
            "prioridad": "MEDIA",
            "accion": "Técnicas de mindfulness",
            "detalle": "El estrés crónico eleva cortisol → resistencia insulina. Practica 10 min/día meditación o yoga.",
            "plazo": "Diario"
        })
    
    if "Conocimiento" in debilidades:
        recomendaciones.append({
            "prioridad": "MEDIA",
            "accion": "Educación en diabetes",
            "detalle": "Participa en taller 'PrevenDiabetes UPCH'. La RD es causa #1 ceguera prevenible (30-80% sin diagnóstico OMS).",
            "plazo": "Próximo ciclo"
        })
    
    if percentil < 25:
        recomendaciones.append({
            "prioridad": "URGENTE",
            "accion": "Seguimiento biopsicosocial",
            "detalle": "Tu perfil está en el 25% inferior. Considera evaluación integral en Bienestar Universitario UPCH.",
            "plazo": "1 mes"
        })
    
    return recomendaciones[:5]  # Máximo 5 recomendaciones
