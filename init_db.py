import sqlite3

def crear_db():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('freestylebot.db')
    cursor = conn.cursor()

    # Crear la tabla de contenido (si no existe)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contenido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,   -- 'video', 'playlist', 'batalla'
        enlace TEXT NOT NULL,
        descripcion TEXT NOT NULL
    );
    """)

    # Insertar contenido (actualiza con tus enlaces reales)
    cursor.execute("""
    INSERT INTO contenido (tipo, enlace, descripcion)
    VALUES
    ('playlist', 'https://youtube.com/playlist?list=PLRB_XTiqd-vaoIXIrnJqoQGoudGo3KLkE&si=KeIovXnznzyweNVp', 'Minutos que te recomendamos escuchar'),
    ('playlist', 'https://youtube.com/playlist?list=PLRB_XTiqd-vbWrIoX1RDUCXCN_4IcMm8W&si=WJooqrOXRwzZus6G', 'Recopilatorios que te podrían gustar'),
    ('batalla', 'https://www.youtube.com/watch?v=cU7C7Fhz4us&list=RDcU7C7Fhz4us&start_radio=1', 'DTOKE vs ARKANO'),
    ('batalla', 'https://www.youtube.com/watch?v=NOgZTOedOpg&list=RDNOgZTOedOpg&start_radio=1', 'GAZIR vs EL MENOR'),
    ('batalla', 'https://www.youtube.com/watch?v=PpsUnUPw7WQ&list=RDPpsUnUPw7WQ&start_radio=1&t=82s', 'DOZER vs ROMA');
    """)

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

# Ejecutar la creación de la base de datos
if __name__ == '__main__':
    crear_db()
    print("Base de datos y tablas creadas exitosamente.")
