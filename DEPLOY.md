# Guía de Despliegue en la Nube

## 📋 ¿Qué es Docker?

Docker es una herramienta que **empaqueta tu aplicación y todas sus dependencias en contenedores** para que funcione igual en cualquier entorno. Imagina que es como una "caja" que contiene todo lo que tu proyecto necesita para funcionar: sistema operativo, librerías, configuraciones, etc.

**Ventajas de Docker:**
- ✅ Funciona igual en tu PC, en el servidor de tu amigo y en la nube
- ✅ No hay problemas de "en mi máquina funciona"
- ✅ Fácil de desplegar y escalar
- ✅ Todo lo necesario está dentro del contenedor

---

## 🚀 Despliegue con Docker Compose (Local)

Primero, probemos que todo funcione localmente con Docker:

### 1. Instalar Docker
- Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop
- Instálalo y ábrelo

### 2. Iniciar todos los servicios
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
docker-compose up -d
```

Esto iniciará:
- 🐘 PostgreSQL (Base de datos)
- 🔄 n8n (Automatización)
- 🏥 Mock HCE (Simulador de Historia Clínica)
- 🔌 API Flask (Backend)
- 📊 Streamlit (Frontend principal)

### 3. Verificar que todo funcione
Abre en tu navegador:
- Streamlit: http://localhost:8501
- n8n: http://localhost:5678
- API: http://localhost:5000/health

### 4. Detener los servicios
```bash
docker-compose down
```

---

## ☁️ Despliegue en la Nube (Opciones Gratuitas)

**Importante:** Render.com tiene limitaciones en el plan gratuito para proyectos con múltiples servicios como este. Aquí tienes varias opciones:

---

### Opción 1: Railway.app (Recomendado para múltiples servicios)

Railway.app es excelente para proyectos con Docker Compose y tiene un plan gratuito generoso.

#### Paso 1: Crear cuenta en Railway
- Ve a: https://railway.app
- Regístrate con GitHub

#### Paso 2: Subir tu proyecto a GitHub
1. Crea un repositorio en GitHub
2. Sube tu proyecto a GitHub:
```bash
git init
git add .
git commit -m "Primer commit"
git remote add origin https://github.com/TU-USUARIO/triage-ia.git
git push -u origin main
```

#### Paso 3: Desplegar en Railway
1. En Railway, haz clic en "New Project" → "Deploy from repo"
2. Selecciona tu repositorio
3. Railway detectará automáticamente tu `docker-compose.yml`
4. Haz clic en "Deploy"

#### Paso 4: Configurar variables de entorno (si es necesario)
Railway configurará automáticamente las variables de entorno necesarias.

#### Paso 5: Acceder a tus servicios
Railway te dará URLs públicas para cada servicio:
- Streamlit: `https://tu-proyecto-streamlit.up.railway.app`
- n8n: `https://tu-proyecto-n8n.up.railway.app`
- API: `https://tu-proyecto-api.up.railway.app`

---

### Opción 2: Render.com (Para servicios individuales)

Si quieres usar Render.com, deberás desplegar cada servicio por separado. El plan gratuito tiene límites, pero funciona para pruebas.

#### Paso 1: Crear cuenta en Render
- Ve a: https://render.com
- Regístrate con GitHub

#### Paso 2: Subir proyecto a GitHub (como en la Opción 1)

#### Paso 3: Desplegar PostgreSQL (Base de Datos)
1. En Render, haz clic en "New" → "PostgreSQL"
2. Nombre: `triage-postgres`
3. Plan: Free
4. Haz clic en "Create Database"
5. Guarda las credenciales (las necesitarás después)

#### Paso 4: Desplegar n8n
1. Haz clic en "New" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Configura:
   - Name: `triage-n8n`
   - Runtime: Docker
   - Dockerfile Path: (usa la imagen oficial de n8n)
   - Environment Variables:
     - `N8N_BASIC_AUTH_ACTIVE`: `true`
     - `N8N_BASIC_AUTH_USER`: `admin`
     - `N8N_BASIC_AUTH_PASSWORD`: `admin123`
     - `N8N_HOST`: `0.0.0.0`
     - `N8N_PORT`: `5678`
4. Haz clic en "Create Web Service"

#### Paso 5: Desplegar API Flask
1. Haz clic en "New" → "Web Service"
2. Conecta tu repositorio
3. Configura:
   - Name: `triage-api`
   - Runtime: Docker
   - Docker Context: `./api`
   - Dockerfile Path: `./api/Dockerfile`
   - Environment Variables:
     - `FLASK_APP`: `app.py`
     - `FLASK_ENV`: `production`
     - `POSTGRES_HOST`: (el host de tu PostgreSQL en Render)
     - `POSTGRES_PORT`: `5432`
     - `POSTGRES_DB`: `triage_ia`
     - `POSTGRES_USER`: (tu usuario de PostgreSQL)
     - `POSTGRES_PASSWORD`: (tu contraseña de PostgreSQL)
     - `HCE_API_URL`: (URL del Mock HCE, lo deployamos después)
4. Haz clic en "Create Web Service"

#### Paso 6: Desplegar Mock HCE
1. Haz clic en "New" → "Web Service"
2. Conecta tu repositorio
3. Configura:
   - Name: `triage-mock-hce`
   - Runtime: Docker
   - Docker Context: `./backend/mock-hce`
   - Dockerfile Path: `./backend/mock-hce/Dockerfile`
4. Haz clic en "Create Web Service"

#### Paso 7: Desplegar Streamlit
1. Haz clic en "New" → "Web Service"
2. Conecta tu repositorio
3. Configura:
   - Name: `triage-streamlit`
   - Runtime: Docker
   - Docker Context: `./frontend/streamlit`
   - Dockerfile Path: `./frontend/streamlit/Dockerfile`
   - Environment Variables:
     - `API_URL`: (URL de tu API en Render)
4. Haz clic en "Create Web Service"

#### Paso 8: Actualizar variables de entorno
Actualiza las variables de entorno de la API con la URL del Mock HCE, y viceversa.

---

### Opción 3: Fly.io (Otra alternativa gratuita)

Fly.io también es excelente para proyectos con Docker. El proceso es similar a Railway.app.

1. Crea una cuenta en: https://fly.io
2. Instala flyctl: https://fly.io/docs/getting-started/installing-flyctl/
3. Despliega con:
```bash
fly launch
fly deploy
```

---

## 🔗 ¿Cómo se conectan los servicios?

Cuando usas Docker Compose, los servicios se pueden comunicar entre sí usando sus nombres:
- Streamlit se conecta a la API usando `http://api:5000`
- La API se conecta a PostgreSQL usando `postgres:5432`
- La API se conecta a Mock HCE usando `http://mock_hce:8001`

En la nube (Railway, Render, etc.), cada servicio tendrá una URL pública y deberás actualizar las variables de entorno para que apunten a esas URLs.

---

## 📝 Credenciales de Prueba

| Servicio | Usuario | Contraseña |
|----------|---------|------------|
| Streamlit | admin | admin123 |
| n8n | admin | admin123 |
| Operador | operador | admin123 |

---

## 🎯 ¿Qué opción elegir?

| Plataforma | Ventajas | Desventajas |
|------------|----------|-------------|
| **Railway.app** | Fácil de usar, soporta Docker Compose, plan gratuito generoso | Límites en el plan gratuito |
| **Render.com** | Buena integración con GitHub, confiable | Debes deployar cada servicio por separado |
| **Fly.io** | Rápido, buena performance | Un poco más técnico de configurar |

**Recomendación:** Emienza con **Railway.app**, es la más fácil y rápida para proyectos con múltiples servicios.

---

## ❓ Preguntas Frecuentes

### ¿Por qué usar Docker?
Porque garantiza que tu aplicación funcione igual en todas partes. No más "en mi máquina funciona".

### ¿Puedo usar otro proveedor de nube?
¡Sí! AWS, Google Cloud, Azure, DigitalOcean, todos soportan Docker.

### ¿El plan gratuito es suficiente?
Para pruebas y proyectos pequeños, sí. Para producción, necesitarás un plan pago.

### ¿Cómo actualizo mi aplicación?
Solo tienes que hacer push a GitHub y la plataforma se encargará de redeployar automáticamente.
