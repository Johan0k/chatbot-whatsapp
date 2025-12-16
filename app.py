import os
import sqlite3
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect('freestylebot.db')
    return conn

# Función para obtener recomendaciones de contenido
def obtener_recomendaciones(tipo):
    conn = conectar_db()
    cursor = conn.cursor()
    query = "SELECT * FROM contenido WHERE tipo=?"
    cursor.execute(query, (tipo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

MENU = (
    "🎤 FreestyleBot\n\n"
    "¿Qué quieres saber sobre freestyle?\n\n"
    "1️⃣ ¿Qué es el freestyle?\n"
    "2️⃣ Origen e historia\n"
    "3️⃣ Referentes y competiciones\n"
    "4️⃣ ¿Se puede vivir del freestyle?\n"
    "5️⃣ Consejos para empezar\n"
    "6️⃣ Recomendaciones de contenido\n"
    "0️⃣ Volver a mostrar el menú"
)

def clean(text):
    return (text or "").strip().lower()

@app.get("/")
def home():
    return "OK - FreestyleBot online", 200

@app.post("/whatsapp")
def whatsapp():
    msg = clean(request.values.get("Body"))
    user = request.values.get("From")
    resp = MessagingResponse()

    if msg in ("hola", "menu", "0"):
        resp.message(MENU)
        return Response(str(resp), mimetype="application/xml")

    if msg == "1":
        resp.message("🎤 El freestyle es la improvisación de rimas en tiempo real, normalmente sobre una base musical. Es una de las formas más puras de rap.")
    elif msg == "2":
        resp.message("📜 El freestyle comenzó en Nueva York en los años 70. Inicialmente como forma de expresión callejera, luego pasó a ser una competencia.")
    elif msg == "3":
        resp.message("🏆 Freestylers: Aczino, Chuty, Wos, Trueno. Competiciones: Red Bull, FMS, God Level.")
    elif msg == "4":
        resp.message("💰 Sí, se puede vivir del freestyle a través de competiciones, shows, música y redes sociales como YouTube o Twitch.")
    elif msg == "5":
        resp.message("🎧 Escucha mucho rap, practica improvisar todos los días, graba tus sesiones y no tengas miedo de equivocarte.")
    elif msg == "6":
        resp.message("🎧 Aquí tienes algunas recomendaciones de freestyle:\n\n")
        # Obtener recomendación de listas de reproducción de freestyle
        playlists = obtener_recomendaciones('playlist')
        for playlist in playlists:
            resp.message(f"Playlist: {playlist[2]}\n{playlist[1]}")  # Descripción y Enlace

        # Obtener recomendaciones de batallas
        batallas = obtener_recomendaciones('batalla')
        for batalla in batallas:
            resp.message(f"Batalla: {batalla[2]}\n{batalla[1]}")  # Descripción y Enlace
        
        return Response(str(resp), mimetype="application/xml")

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

