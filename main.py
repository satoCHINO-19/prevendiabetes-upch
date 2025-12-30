from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from analysis import analizar_tendencias, generar_recomendaciones
import pandas as pd

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PrevenDiabetes UPCH - Sistema RSU",
    description="Encuesta de prevención de diabetes en universitarios basada en investigación doctoral",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

PREGUNTAS = [
    ("A. CONOCIMIENTO SOBRE DIABETES", [
        "Mi conocimiento sobre qué es la diabetes mellitus es:",
        "Mi comprensión de las diferencias entre diabetes tipo 1, tipo 2 y gestacional es:",
        "Mi conocimiento sobre complicaciones de la diabetes (retinopatía, nefropatía, neuropatía) es:",
        "Mi conocimiento sobre factores de riesgo genéticos y ambientales de la diabetes es:",
        "Mi conocimiento sobre la importancia del diagnóstico temprano de la diabetes es:"
    ]),
    ("B. HÁBITOS ALIMENTARIOS", [
        "La calidad de mi dieta (consumo de frutas, verduras, fibra, agua) es:",
        "Mi frecuencia de consumo de alimentos ultraprocesados es: (Malo=nunca, Excelente=siempre)",
        "Mi control sobre el tamaño de las porciones que consumo es:",
        "La frecuencia con la que desayuno es:",
        "Mi hábito de leer etiquetas nutricionales antes de comprar alimentos es:"
    ]),
    ("C. ACTIVIDAD FÍSICA", [
        "Mi nivel de actividad física semanal (caminar, deporte, ejercicio) es:",
        "La cantidad de tiempo que paso sentado/a al día es: (Malo=poco, Excelente=mucho)",
        "Mi constancia en realizar ejercicio aeróbico es:",
        "Mi conocimiento sobre los beneficios del ejercicio en prevención de diabetes es:"
    ]),
    ("D. ANTECEDENTES Y CONTROL PERSONAL", [
        "Mi conocimiento sobre si tengo familiares directos con diabetes es:",
        "Mi control sobre mi peso corporal (IMC, perímetro abdominal) es:",
        "Mi frecuencia de chequeos médicos preventivos es:",
        "Mi preocupación por mi riesgo personal de desarrollar diabetes es:"
    ]),
    ("E. SALUD MENTAL Y ESTRÉS", [
        "Mi manejo del estrés académico/laboral es:",
        "La calidad de mis horas de sueño diarias (7-8 horas) es:",
        "Mi percepción del impacto del estrés en mi salud física es:"
    ]),
    ("F. PERCEPCIÓN DE PREVENCIÓN", [
        "Mi interés por participar en programas de prevención de diabetes es:",
        "Mi disposición a cambiar hábitos si me informan que tengo riesgo es:",
        "Mi confianza en que la prevención es más efectiva que el tratamiento tardío es:"
    ])
]

INVERTIDAS = [7, 12]

@app.get("/", response_class=HTMLResponse)
async def mostrar_encuesta(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "secciones": PREGUNTAS
    })

@app.post("/enviar", response_class=HTMLResponse)
async def procesar_encuesta(
    request: Request,
    nombre: str = Form(None),
    edad: int = Form(...),
    genero: str = Form(...),
    facultad: str = Form(None),
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    
    # Capturar respuestas
    respuestas = {}
    for i in range(1, 25):
        valor = int(form_data.get(f"p{i}"))
        if i in INVERTIDAS:
            valor = 5 - valor  # Invertir
        respuestas[f"p{i}"] = valor
    
    # Calcular puntajes por dimensión
    puntaje_conocimiento = sum([respuestas[f"p{i}"] for i in range(1, 6)])
    puntaje_alimentacion = sum([respuestas[f"p{i}"] for i in range(6, 11)])
    puntaje_actividad = sum([respuestas[f"p{i}"] for i in range(11, 15)])
    puntaje_antecedentes = sum([respuestas[f"p{i}"] for i in range(15, 19)])
    puntaje_estres = sum([respuestas[f"p{i}"] for i in range(19, 22)])
    puntaje_prevencion = sum([respuestas[f"p{i}"] for i in range(22, 25)])
    
    puntaje_total = (puntaje_conocimiento + puntaje_alimentacion + 
                     puntaje_actividad + puntaje_antecedentes + 
                     puntaje_estres + puntaje_prevencion)
    
    # Categorizar
    if puntaje_total <= 48:
        categoria = "Riesgo Alto"
        color = "red"
    elif puntaje_total <= 72:
        categoria = "Riesgo Moderado"
        color = "orange"
    else:
        categoria = "Buena Prevención"
        color = "green"
    
    # Analizar tendencias
    tendencias = analizar_tendencias(edad, genero, facultad, respuestas, db)
    
    # Generar recomendaciones
    recomendaciones = generar_recomendaciones(
        categoria, 
        tendencias["debilidades"], 
        tendencias["percentil"]
    )
    
    # Guardar en BD
    nueva_encuesta = models.Encuesta(
        nombre=nombre,
        edad=edad,
        genero=genero,
        facultad=facultad,
        **respuestas,
        puntaje_total=puntaje_total,
        puntaje_conocimiento=puntaje_conocimiento,
        puntaje_alimentacion=puntaje_alimentacion,
        puntaje_actividad=puntaje_actividad,
        puntaje_antecedentes=puntaje_antecedentes,
        puntaje_estres=puntaje_estres,
        puntaje_prevencion=puntaje_prevencion,
        categoria_riesgo=categoria
    )
    db.add(nueva_encuesta)
    db.commit()
    
    return templates.TemplateResponse("resultado.html", {
        "request": request,
        "puntaje": puntaje_total,
        "categoria": categoria,
        "color": color,
        "dimensiones": {
            "Conocimiento": (puntaje_conocimiento, 20),
            "Alimentación": (puntaje_alimentacion, 20),
            "Actividad": (puntaje_actividad, 16),
            "Antecedentes": (puntaje_antecedentes, 16),
            "Estrés": (puntaje_estres, 12),
            "Prevención": (puntaje_prevencion, 12)
        },
        "tendencias": tendencias,
        "recomendaciones": recomendaciones
    })

@app.get("/estadisticas", response_class=HTMLResponse)
async def estadisticas(request: Request, db: Session = Depends(get_db)):
    encuestas = db.query(models.Encuesta).all()
    
    if not encuestas:
        return templates.TemplateResponse("estadisticas.html", {
            "request": request,
            "stats": {
                "total": 0,
                "promedio": 0,
                "por_categoria": {},
                "por_facultad": {},
                "por_genero": {}
            }
        })
    
    df = pd.DataFrame([{
        "edad": e.edad,
        "genero": e.genero,
        "facultad": e.facultad,
        "puntaje": e.puntaje_total,
        "categoria": e.categoria_riesgo
    } for e in encuestas])
    
    stats = {
        "total": len(df),
        "promedio": round(df['puntaje'].mean(), 2),
        "por_categoria": df['categoria'].value_counts().to_dict(),
        "por_facultad": df.groupby('facultad')['puntaje'].mean().to_dict(),
        "por_genero": df.groupby('genero')['puntaje'].mean().to_dict()
    }
    
    return templates.TemplateResponse("estadisticas.html", {
        "request": request,
        "stats": stats
    })

@app.get("/api/tendencias")
async def api_tendencias(db: Session = Depends(get_db)):
    """Endpoint para análisis de tendencias (para dashboard externo)"""
    encuestas = db.query(models.Encuesta).all()
    
    if not encuestas:
        return JSONResponse({"error": "No hay datos disponibles"})
    
    df = pd.DataFrame([{
        "edad": e.edad,
        "puntaje": e.puntaje_total,
        "categoria": e.categoria_riesgo,
        "facultad": e.facultad
    } for e in encuestas])
    
    return JSONResponse({
        "tendencia_general": {
            "media": float(df['puntaje'].mean()),
            "desviacion": float(df['puntaje'].std()),
            "percentil_25": float(df['puntaje'].quantile(0.25)),
            "percentil_75": float(df['puntaje'].quantile(0.75))
        },
        "por_edad": df.groupby('edad')['puntaje'].mean().to_dict(),
        "distribucion_riesgo": df['categoria'].value_counts().to_dict()
    })
