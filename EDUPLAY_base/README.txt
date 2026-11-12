EDUPLAY - plantilla inicial con Flask + SQLite

ESTRUCTURA
- app.py: rutas, inicio de sesión, registro y API de resultados.
- eduplay.db: se crea automáticamente al ejecutar la app.
- templates/: páginas HTML.
- static/css/estilos.css: diseño.
- static/js/funciones.js: revisión de respuestas con JavaScript.
- requirements.txt: dependencia necesaria.

CÓMO EJECUTAR EN VS CODE (Windows)
1. Abre esta carpeta en Visual Studio Code.
2. Abre Terminal > New Terminal.
3. (Opcional, recomendado) crea un entorno virtual:
   python -m venv venv
   venv\Scripts\activate
4. Instala Flask:
   python -m pip install -r requirements.txt
5. Ejecuta:
   python app.py
6. Abre en tu navegador la dirección que muestra Flask, normalmente:
   http://127.0.0.1:5000

NOTAS IMPORTANTES
- No borres ni reemplaces tu proyecto actual sin hacer una copia. Esta es una plantilla aparte.
- Cambia app.secret_key por una clave larga y privada antes de publicar.
- debug=True es solo para desarrollo local; no lo uses en producción.
- Esta plantilla es para aprender y probar localmente. Antes de publicarla para usuarios reales, agrega protección CSRF, límites de intentos de inicio de sesión, configuración segura de cookies y una clave secreta desde variables de entorno.
- Las contraseñas se guardan como hash, no en texto plano.
- Las preguntas y respuestas de demostración están en static/js/funciones.js y en templates/lectura.html / templates/matematicas.html.
- No incluye flashcards. Las actividades se presentan como cuestionarios.
