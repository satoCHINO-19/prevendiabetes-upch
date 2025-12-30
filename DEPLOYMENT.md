# 🚀 GUÍA DE DEPLOYMENT - PrevenDiabetes UPCH

## Opción 1: Render (RECOMENDADO - 100% GRATIS)

### Paso 1: Subir a GitHub

```bash
# Desde la carpeta del proyecto
git init
git add .
git commit -m "🩺 Sistema PrevenDiabetes UPCH - Encuesta RSU"
git branch -M main

# Crear repositorio en GitHub (github.com/new)
# Luego conectarlo:
git remote add origin https://github.com/TU-USUARIO/prevendiabetes-upch.git
git push -u origin main
```

### Paso 2: Deploy en Render

1. Ve a [render.com](https://render.com) y regístrate (gratis)
2. Click en "New +" → "Web Service"
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `prevendiabetes-upch`
5. Configuración:
   - **Name**: `prevendiabetes-upch` (o el que prefieras)
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python data_simulator.py
     ```
   - **Start Command**: 
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: Free

6. Click "Create Web Service"
7. Espera 3-5 minutos mientras se despliega
8. ¡Listo! Tendrás una URL tipo: `https://prevendiabetes-upch.onrender.com`

### Importante para Render:
- El servicio gratuito se "duerme" después de 15 minutos de inactividad
- Tarda ~30 segundos en "despertar" cuando alguien lo visita
- Tiene 750 horas gratuitas al mes (más que suficiente)
- La BD SQLite se mantiene entre despliegues

---

## Opción 2: Railway (También GRATIS)

### Paso 1: Igual que Render (subir a GitHub)

### Paso 2: Deploy en Railway

1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detecta automáticamente Python y hace todo solo
6. Te da una URL tipo: `https://prevendiabetes-upch.up.railway.app`

### Ventajas de Railway:
- Más rápido (no se duerme)
- $5 de crédito gratis al mes
- Deploy automático en cada push a GitHub

---

## Opción 3: PythonAnywhere (Alternativa)

1. Crea cuenta en [pythonanywhere.com](https://www.pythonanywhere.com) (gratis)
2. Sube los archivos via Web
3. Configura WSGI manual
4. Menos automático pero funciona

---

## 📸 EVIDENCIA PARA EL PROFE

Una vez desplegado, captura:

1. **URL pública** (ej: https://prevendiabetes-upch.onrender.com)
2. **Screenshot del formulario funcionando**
3. **Screenshot de las estadísticas con 200+ registros**
4. **Panel de Render/Railway mostrando fecha/hora de deploy**

---

## 🔧 Si algo falla:

### Error 1: "Module not found"
**Solución**: Asegúrate que requirements.txt esté en la raíz del proyecto

### Error 2: "Database locked"
**Solución**: En el build command, ejecuta primero data_simulator.py:
```bash
pip install -r requirements.txt && python data_simulator.py
```

### Error 3: "Port already in use"
**Solución**: El comando debe usar `$PORT` en vez de un puerto fijo:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ CHECKLIST FINAL

- [ ] Código en GitHub
- [ ] Web service creado en Render/Railway
- [ ] URL pública funciona
- [ ] Encuesta se puede llenar
- [ ] Estadísticas muestran 200+ registros
- [ ] Screenshots capturados para evidencia
- [ ] URL compartida con el profe

---

**Tiempo estimado total: 15-20 minutos** ⏱️

¡Éxito con tu proyecto RSU! 🎓
