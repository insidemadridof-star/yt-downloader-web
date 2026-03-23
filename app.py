from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Ruta principal (home)
@app.route('/')
def home():
    return render_template('index.html')


# Ruta para descargar el vídeo
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "Error: No URL provided", 400

    # Nombre único para evitar conflictos
    filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Error descargando el vídeo: {str(e)}", 500

    finally:
        # Borra el archivo después de enviarlo (opcional pero recomendable)
        if os.path.exists(filename):
            os.remove(filename)


# ⚠️ IMPORTANTE: NO poner app.run()
# Render usa gunicorn, no este bloque
