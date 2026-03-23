from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Página principal
@app.route('/')
def home():
    return render_template('index.html')


# Ruta para descargar vídeo
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "Error: No URL provided", 400

    # Nombre único para evitar conflictos
    filename = f"{uuid.uuid4()}.mp4"

    # 🔥 CONFIGURACIÓN OPTIMIZADA yt-dlp
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': filename,
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Error descargando el vídeo: {str(e)}", 500

    finally:
        # Borra el archivo después de enviarlo
        if os.path.exists(filename):
            os.remove(filename)


# ⚠️ NO añadir app.run() (Render usa gunicorn)
