import random
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def generar_respuesta_correlacionada(base, varianza=1):
    """Genera respuestas con tendencia realista"""
    return max(1, min(4, base + random.randint(-varianza, varianza)))

def simular_encuestas(n=200):
    db = SessionLocal()
    
    facultades = ["Medicina", "Estomatología", "Enfermería", "Obstetricia", 
                  "Tecnología Médica", "Psicología", "Ciencias", "Administración"]
    
    for i in range(n):
        # Perfil base aleatorio
        edad = random.randint(17, 28)
        genero = random.choice(["M", "F", "Otro"])
        facultad = random.choice(facultades)
        
        # Perfiles de riesgo (30% alto, 50% moderado, 20% bajo)
        perfil = random.choices(["alto", "moderado", "bajo"], weights=[0.3, 0.5, 0.2])[0]
        
        if perfil == "alto":
            base_conocimiento = 2
            base_alimentacion = 2
            base_actividad = 1
            base_estres = 2
        elif perfil == "moderado":
            base_conocimiento = 3
            base_alimentacion = 2
            base_actividad = 2
            base_estres = 2
        else:
            base_conocimiento = 3
            base_alimentacion = 3
            base_actividad = 3
            base_estres = 3
        
        # Generar respuestas con correlación
        respuestas = {
            # Conocimiento
            "p1": generar_respuesta_correlacionada(base_conocimiento),
            "p2": generar_respuesta_correlacionada(base_conocimiento),
            "p3": generar_respuesta_correlacionada(base_conocimiento),
            "p4": generar_respuesta_correlacionada(base_conocimiento),
            "p5": generar_respuesta_correlacionada(base_conocimiento, 0),
            # Alimentación
            "p6": generar_respuesta_correlacionada(base_alimentacion),
            "p7": generar_respuesta_correlacionada(4 - base_alimentacion),  # Invertida
            "p8": generar_respuesta_correlacionada(base_alimentacion),
            "p9": generar_respuesta_correlacionada(base_alimentacion),
            "p10": generar_respuesta_correlacionada(base_alimentacion),
            # Actividad
            "p11": generar_respuesta_correlacionada(base_actividad),
            "p12": generar_respuesta_correlacionada(4 - base_actividad),  # Invertida
            "p13": generar_respuesta_correlacionada(base_actividad),
            "p14": generar_respuesta_correlacionada(base_conocimiento),
            # Antecedentes
            "p15": random.randint(2, 4),
            "p16": generar_respuesta_correlacionada(base_actividad),
            "p17": generar_respuesta_correlacionada(base_conocimiento - 1),
            "p18": generar_respuesta_correlacionada(base_conocimiento),
            # Estrés
            "p19": generar_respuesta_correlacionada(base_estres),
            "p20": generar_respuesta_correlacionada(base_estres),
            "p21": generar_respuesta_correlacionada(base_conocimiento),
            # Prevención
            "p22": generar_respuesta_correlacionada(base_conocimiento),
            "p23": generar_respuesta_correlacionada(base_conocimiento),
            "p24": 4 if random.random() > 0.2 else 3,
        }
        
        # Calcular puntajes
        puntaje_conocimiento = sum([respuestas[f"p{i}"] for i in range(1, 6)])
        puntaje_alimentacion = sum([respuestas[f"p{i}"] for i in range(6, 11)])
        puntaje_actividad = sum([respuestas[f"p{i}"] for i in range(11, 15)])
        puntaje_antecedentes = sum([respuestas[f"p{i}"] for i in range(15, 19)])
        puntaje_estres = sum([respuestas[f"p{i}"] for i in range(19, 22)])
        puntaje_prevencion = sum([respuestas[f"p{i}"] for i in range(22, 25)])
        
        # Ajustar invertidas
        puntaje_alimentacion += (5 - respuestas["p7"]) - respuestas["p7"]
        puntaje_actividad += (5 - respuestas["p12"]) - respuestas["p12"]
        
        puntaje_total = (puntaje_conocimiento + puntaje_alimentacion + 
                         puntaje_actividad + puntaje_antecedentes + 
                         puntaje_estres + puntaje_prevencion)
        
        if puntaje_total <= 48:
            categoria = "Riesgo Alto"
        elif puntaje_total <= 72:
            categoria = "Riesgo Moderado"
        else:
            categoria = "Buena Prevención"
        
        nueva_encuesta = models.Encuesta(
            nombre=f"Estudiante_{i+1}" if random.random() > 0.3 else None,
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
    db.close()
    print(f"✅ {n} encuestas simuladas generadas correctamente")

if __name__ == "__main__":
    simular_encuestas(200)
