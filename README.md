# PrevenDiabetes UPCH

Sistema web de evaluación de riesgo de Diabetes Mellitus en universitarios, desarrollado como proyecto de **Responsabilidad Social Universitaria (RSU)** de UPCH.

## Objetivos
- Sensibilizar sobre prevención de DM en población universitaria
- Generar data para investigación en salud pública
- Ofrecer recomendaciones personalizadas basadas en evidencia

## Fundamentación Científica
Basado en la tesis doctoral:  
**"Modelo de prediagnóstico para identificación de DM aplicando Red de Creencias Profundas (DBN)"**  
- INEI 2021: 69.7% diagnósticos tardíos en Perú
- DBN alcanza 95.7% precisión en prediagnóstico
- RD: causa #1 de ceguera prevenible

## Instalación y Ejecución

### Local
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/prevendiabetes-upch.git
cd prevendiabetes-upch

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Generar BD simulada (200 registros)
python data_simulator.py

# 5. Ejecutar servidor
uvicorn main:app --reload

# 6. Abrir en navegador
http://127.0.0.1:8000
```

### Render
Configuración:
   - **Build Command**: `pip install -r requirements.txt && python data_simulator.py`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3

## Endpoints

- `/` - Encuesta interactiva
- `/estadisticas` - Dashboard público
- `/api/tendencias` - API REST para análisis

## Tecnologías

- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: TailwindCSS
- **Análisis**: Pandas + NumPy + Scikit-learn
- **BD**: SQLite (dev) / PostgreSQL (prod)

## Características

✅ Encuesta validada de 24 ítems (escala Likert)  
✅ Análisis de tendencias comparativo  
✅ Recomendaciones personalizadas basadas en evidencia  
✅ Dashboard de estadísticas en tiempo real  
✅ Base de datos simulada con 200 registros  
✅ API REST para integración externa  

## Autor

**Proyecto RSU - Universidad Peruana Cayetano Heredia**  
Desarrollado para: Prof. Jaime Escobar Aguirre  
Año: 2025

## Licencia

Proyecto académico de Responsabilidad Social Universitaria
