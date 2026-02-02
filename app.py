import os
import sqlite3
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from openai import OpenAI

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

if not DEEPSEEK_API_KEY:
    raise RuntimeError("Falta DEEPSEEK_API_KEY en variables de entorno.")






BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "freestylebot.db")


def conectar_db():
    return sqlite3.connect(DB_PATH)

def obtener_recomendaciones(tipo: str):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contenido WHERE tipo=?", (tipo,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def recomendaciones_formato():
    playlists = obtener_recomendaciones("playlist")
    batallas = obtener_recomendaciones("batalla")

    lines = []
    if playlists:
        lines.append("Minutos que te recomendamos escuchar:")
        for p in playlists:
            # Asumiendo: (id, enlace, descripcion, tipo) o similar.
            # En tu código anterior usabas [2]=desc, [1]=enlace
            lines.append(f"- {p[2]}: {p[1]}")
        lines.append("")

    if batallas:
        lines.append("Batallas que recomienda el bot:")
        for b in batallas:
            lines.append(f"- {b[2]}: {b[1]}")

    if not lines:
        return "Aún no tengo recomendaciones cargadas en la base de datos."
    return "\n".join(lines)

# -----------------------------
# UX: menú (ayuda) + limpieza
# -----------------------------
MENU = (
    "FreestyleBot (IA)\n\n"
    "Escribe tu pregunta libre sobre freestyle o usa:\n\n"
    "menu  -> ver este menú\n"
    "recomendaciones -> links curados\n"
    "reset -> borrar contexto\n\n"
    "Ejemplos:\n"
    "- ¿De dónde viene el freestyle?\n"
    "- ¿Se puede vivir del freestyle? ¿Cómo?\n"
    "- Dame referentes y por qué son importantes\n"
)

def clean(text):
    return (text or "").strip()

def clip(text: str, max_chars: int = 1200):
    text = (text or "").strip()
    return text if len(text) <= max_chars else text[:max_chars] + "\n\n(Escriba 'continuar' para seguir)"


# -----------------------------
# Memoria corta (in-memory)
# Nota: en serverless puede reiniciarse.
# -----------------------------
_memory = {}  # { user_id: [("user", "..."), ("assistant", "..."), ...] }

def get_history(user_id: str, limit_pairs: int = 4):
    msgs = _memory.get(user_id, [])
    # limit_pairs = pares user/assistant; 2 mensajes por par
    max_msgs = limit_pairs * 2
    return msgs[-max_msgs:]

def add_history(user_id: str, role: str, content: str):
    _memory.setdefault(user_id, []).append((role, content))

def reset_history(user_id: str):
    _memory.pop(user_id, None)

# -----------------------------
# IA: función principal
# -----------------------------
SYSTEM_STYLE = (
    "Eres FreestyleBot, un asistente experto en freestyle rap y cultura de batallas.\n"
    "Objetivo: responder preguntas sobre historia, referentes, competiciones, cultura, y cómo se monetiza.\n"
    "Estilo: profesional pero juvenil, claro, directo, sin relleno.\n"
    "Accesibilidad: usa lenguaje simple, explica términos si el usuario parece novato.\n"
    "Manejo de errores: si la pregunta es ambigua, haz UNA pregunta de aclaración.\n"
    "Seguridad/copyright: NO entregues letras completas de canciones. Si piden letras, resume o explica el tema.\n"
    "Formato: si ayuda, usa bullets y mini-secciones (2–6 líneas)."
)

def ask_ai(user_text: str, user_id: str):
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    curated = ""
    lowered = user_text.lower()
    if any(k in lowered for k in ["recomend", "playlist", "batalla", "batallas", "ver videos", "ver vídeos"]):
        curated = (
            "\n\nRECOMENDACIONES CURADAS (si el usuario pide links o qué ver):\n"
            + recomendaciones_formato()
        )

    history = get_history(user_id)

    messages = [{"role": "system", "content": SYSTEM_STYLE + curated}]

    for role, content in history:
        # Tu memoria guarda ("user"/"assistant", texto), esto calza perfecto aquí
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_text})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.8,
        max_tokens=350
    )

    answer = resp.choices[0].message.content
    return (answer or "").strip()


# -----------------------------
# Endpoints
# -----------------------------
@app.get("/")
def home():
    return "OK - FreestyleBot online", 200

@app.post("/whatsapp")
def whatsapp():
    msg = clean(request.values.get("Body"))
    user = request.values.get("From") or "unknown"
    resp = MessagingResponse()

    if not msg:
        resp.message("Escribe una pregunta o escribe 'menu'.")
        return Response(str(resp), mimetype="application/xml")

    cmd = msg.lower()

    # Comandos UX
    if cmd in ("hola", "menu", "help", "ayuda"):
        resp.message(MENU)
        return Response(str(resp), mimetype="application/xml")

    if cmd == "reset":
        reset_history(user)
        resp.message("Listo. Contexto reiniciado. Ahora escribe tu pregunta.")
        return Response(str(resp), mimetype="application/xml")

    if cmd in ("recomendaciones", "recom", "6"):
        # Puedes responder directo sin IA (más confiable) o pedirle a la IA que lo “narre”.
        resp.message(recomendaciones_formato())
        return Response(str(resp), mimetype="application/xml")

    # IA: guardar turno, responder, guardar respuesta
    try:
        add_history(user, "user", msg)
        answer = ask_ai(msg, user)
        add_history(user, "assistant", answer)
        resp.message(clip(answer))

    except Exception as e:
        print("ERROR IA:", repr(e))
        resp.message("Hubo un error procesando tu mensaje. Revisa la consola del servidor.")
    

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
