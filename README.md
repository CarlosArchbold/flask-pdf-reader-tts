# 📄 Lector de PDF Local con Texto a Voz (TTS)

Este es un proyecto completo que combina un backend robusto en **Flask (Python)** y una interfaz web interactiva en **HTML, CSS y JavaScript** para cargar archivos PDF, procesar su contenido de texto y transformarlo en audio hablado en tiempo real.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3, Flask, PyPDF2 (o la librería utilizada para la extracción), gTTS / pyttsx3 (Librería de texto a voz).
*   **Frontend:** HTML5, CSS3, JavaScript (Fetch API para comunicación asíncrona).

---

## 🚀 Características del Proyecto

*   **Carga de PDF:** Interfaz limpia para arrastrar o seleccionar archivos locales.
*   **Procesamiento Inteligente:** Extracción exacta del texto contenido en las páginas del PDF.
*   **Conversión TTS (Text-to-Speech):** Reproducción de audio fluida directamente en el navegador.

---

## 📂 Estructura del Repositorio

*   📁 `backend/`: Contiene la API de Flask, rutas de procesamiento, lógicas de conversión de voz y gestión de archivos temporales.
*   📁 `frontend/`: Archivos de interfaz web (`index.html`, estilos y scripts) encargados de renderizar la aplicación y controlar los reproductores de audio.
