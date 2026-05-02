# 🚀 Guía PASO A PASO para desplegar tu proyecto en Railway.app

¡Esta guía es ESPECÍFICA para tu proyecto de triaje IA! Sigue estos pasos y estarás online en pocos minutos.

---

## 📋 Requisitos previos

1. ✅ Tener tu proyecto listo (lo tienes!)
2. ✅ Tener una cuenta en GitHub (si no, créala primero)
3. ✅ Tener una cuenta en Railway.app (es gratuita!)

---

## Paso 1: Subir tu proyecto a GitHub

### 1.1 Inicializar Git (si no lo has hecho)
Abre una terminal en la carpeta de tu proyecto y ejecuta:
```bash
git init
```

### 1.2 Crear un repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre del repositorio: `triage-ia` (o el nombre que quieras)
3. Elige **Public** o **Private** (como prefieras)
4. **NO** marques las opciones de "Initialize this repository" (ya tienes tu código)
5. Haz clic en **Create repository**

### 1.3 Subir tu código a GitHub
Ejecuta estos comandos en la terminal (cambia `TU-USUARIO` por tu nombre de usuario de GitHub):
```bash
git add .
git commit -m "Primer commit - Proyecto de triaje IA"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/triage-ia.git
git push -u origin main
```

¡Listo! Tu código ya está en GitHub.

---

## Paso 2: Desplegar en Railway.app

### 2.1 Crear cuenta en Railway
1. Ve a https://railway.app
2. Haz clic en **Sign Up**
3. Elige **Sign up with GitHub** (más fácil)
4. Autoriza a Railway para acceder a tus repositorios

### 2.2 Crear un nuevo proyecto en Railway
1. En el dashboard de Railway, haz clic en **New Project**
2. Selecciona **Deploy from repo**
3. Haz clic en **Configure GitHub App** (para dar acceso a tu repositorio)
4. Selecciona tu repositorio `triage-ia`
5. Vuelve a Railway y selecciona tu repositorio

### 2.3 Configurar el despliegue
1. Railway detectará automáticamente tu `docker-compose.yml`
2. Revisa la configuración (debería estar bien por defecto)
3. Haz clic en **Deploy**

### 2.4 Esperar a que termine el despliegue
- Railway mostrará un indicador de progreso
- Esto puede tardar de 2 a 5 minutos
- Cuando termine, verás un checkmark ✅ verde

---

## Paso 3: Acceder a tus servicios

¡Felicidades! Tu proyecto ya está en línea. Railway te dará URLs públicas para cada servicio:

| Servicio | URL de ejemplo | Credenciales |
|----------|----------------|--------------|
| 📊 Streamlit (Frontend principal) | `https://triage-ia-streamlit.up.railway.app` | admin / admin123 |
| 🔄 n8n (Automatización) | `https://triage-ia-n8n.up.railway.app` | admin / admin123 |
| 🔌 API Flask | `https://triage-ia-api.up.railway.app` | - |
| 🏥 Mock HCE | `https://triage-ia-mock-hce.up.railway.app` | - |

Las URLs reales las verás en el dashboard de Railway.

---

## Paso 4: Configurar variables de entorno (si es necesario)

Railway configura automáticamente la mayoría de las variables, pero si necesitas cambiar algo:

1. Ve a tu proyecto en Railway
2. Haz clic en el servicio que quieras configurar (ej: `api`)
3. Ve a la pestaña **Variables**
4. Agrega o modifica las variables que necesites

Las variables importantes:
- `POSTGRES_HOST`: Railway lo configura automáticamente
- `POSTGRES_PORT`: `5432`
- `POSTGRES_DB`: `triage_ia`
- `POSTGRES_USER`: Railway lo configura
- `POSTGRES_PASSWORD`: Railway lo configura
- `HCE_API_URL`: La URL del servicio `mock-hce` en Railway
- `API_URL`: La URL del servicio `api` en Railway (para Streamlit)

---

## Paso 5: Probar tu aplicación

1. Abre la URL de Streamlit en tu navegador
2. Inicia sesión con `admin` / `admin123`
3. Prueba crear un triaje, buscar pacientes, etc.
4. Abre la URL de n8n y configura los workflows si quieres

---

## 🔄 ¿Cómo actualizar tu aplicación?

Cuando hagas cambios en tu código:
1. Haz commit y push a GitHub:
```bash
git add .
git commit -m "Descripción de los cambios"
git push
```
2. Railway detectará automáticamente el push y redeployará tu aplicación
3. Espera 1-2 minutos y los cambios estarán en línea

---

## 💡 Tips útiles

1. **Logs**: En Railway, haz clic en cualquier servicio y ve a la pestaña **Logs** para ver los registros
2. **Monitoreo**: Railway te muestra métricas de uso (CPU, memoria, etc.)
3. **Dominios personalizados**: Si quieres usar tu propio dominio, Railway lo permite
4. **Backups**: Railway hace backups automáticos de tu base de datos

---

## ❓ Problemas comunes y soluciones

### Problema: El despliegue falla
- Solución: Ve a los **Logs** del servicio para ver el error
- Asegúrate de que todos los archivos necesarios estén en GitHub

### Problema: Los servicios no se conectan entre sí
- Solución: Verifica las variables de entorno, especialmente las URLs de los servicios
- En Railway, los servicios se pueden comunicar usando sus nombres internos

### Problema: Se agotan los límites del plan gratuito
- Solución: Considera actualizar a un plan pago o eliminar servicios que no uses

---

## 🎉 ¡Listo!

Tu proyecto ya está en la nube y accesible desde cualquier PC con solo abrir el enlace. ¡Felicitaciones!

Si tienes alguna duda o problema, ¡avísame!
