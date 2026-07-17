import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pypdf import PdfReader
from deep_translator import GoogleTranslator
from gtts import gTTS

app = Flask(__name__)
# CORS permite que tu frontend se comunique con el backend sin bloqueos de seguridad
CORS(app)

# Carpetas temporales para guardar los PDFs subidos y los audios generados
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audios'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    """
    Este endpoint recibe el PDF, extrae el texto, 
    lo traduce opcionalmente al español y genera el archivo de audio MP3.
    ¡Todo 100% gratis!
    """
    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400
    
    file = request.files['file']
    should_translate = request.form.get('translate', 'false').lower() == 'true'
    
    if file.filename == '':
        return jsonify({"error": "Archivo no seleccionado"}), 400

    # 1. Guardar el archivo PDF temporalmente
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    try:
        # 2. Extraer el texto usando pypdf (Gratis y local)
        reader = PdfReader(pdf_path)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        if not extracted_text.strip():
            return jsonify({"error": "No se pudo extraer texto de este PDF (¿es una imagen o está escaneado?)"}), 400

        # 3. Traducir si el usuario lo solicitó (Gratis e ilimitado con deep_translator)
        final_text = extracted_text
        lang = 'en'  # Idioma original por defecto (Inglés)
        
        if should_translate:
            # Traducimos de inglés (en) a español (es)
            # Nota: Dividimos en bloques si el texto es excesivamente largo
            final_text = GoogleTranslator(source='auto', target='es').translate(extracted_text[:4500])
            lang = 'es'

        # 4. Convertir texto a voz (Gratis con gTTS)
        tts = gTTS(text=final_text[:1000], lang=lang, slow=False) # Limitamos a 1000 caracteres para pruebas rápidas
        audio_filename = f"audio_{os.path.splitext(file.filename)[0]}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        tts.save(audio_path)

        # 5. Responder al frontend con el texto procesado y el nombre del audio para reproducir
        return jsonify({
            "text": final_text,
            "audio_url": f"/get-audio/{audio_filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Limpieza: Eliminamos el PDF temporal para no saturar el disco
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@app.route('/get-audio/<filename>', methods=['GET'])
def get_audio(filename):
    """Devuelve el archivo de audio generado para que el navegador lo reproduzca"""
    return send_file(os.path.join(AUDIO_FOLDER, filename), mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True, port=5000)