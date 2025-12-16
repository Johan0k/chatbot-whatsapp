# **FreestyleBot: Chatbot de WhatsApp para Freestyle**

**FreestyleBot** es un chatbot interactivo creado con **Flask** y **Twilio** para **WhatsApp**. Este bot está diseñado para responder preguntas sobre el mundo del **freestyle rap**, proporcionar **consejos útiles**, **recomendaciones de contenido** (como batallas, canciones, playlists), y mucho más. Desarrollado como parte del examen final en la materia de **Interacción Humano-Computador**, el bot fue **desplegado en Vercel** para que sea accesible públicamente.



## **Características**

- **Responde preguntas sobre freestyle**: Ofrece respuestas detalladas sobre qué es el freestyle, su historia, competiciones y referentes.
- **Recomendaciones de contenido**: El bot puede recomendar videos de freestyle, batallas, y playlists.
- **Interacción fluida**: El flujo de conversación es simple y directo, con opciones claras para que los usuarios interactúen.
- **Desplegado en Vercel**: El bot está disponible 24/7 y accesible desde cualquier lugar a través de **WhatsApp**.

## **Tecnologías utilizadas**

- **Python 3.8+**
- **Flask 2.2.2**: Framework web para la construcción del backend.
- **Twilio API**: Para integrar WhatsApp con el bot.
- **SQLite 3.0**: Base de datos ligera para almacenar recomendaciones de contenido.
- **Vercel**: Plataforma de despliegue en la nube.

## **Instalación**

 **Clonar el repositorio**:

   ```bash
   git clone https://github.com/Johan0k/chatbot-whatsapp.git
   cd chatbot-whatsapp

   pip install -r requirements.txt
   python init_db.py


``````
  

**Uso**: 


### **Ejecutar localmente**

Para ejecutar el bot en tu máquina local:

1. Asegúrate de que **Flask** esté instalado y las dependencias estén configuradas.
2. Ejecuta el servidor Flask:

   ```bash
   python app.py

## **Configuración de Twilio**

Para que el bot funcione con **WhatsApp** a través de Twilio, sigue estos pasos:

1. **Crear una cuenta en Twilio**: Regístrate en [Twilio](https://www.twilio.com/).
2. **Unirse al Sandbox de WhatsApp**: Ve a **Twilio Console** → **Messaging** → **Try it out** → **Send a WhatsApp message** y sigue las instrucciones para unirte al **WhatsApp Sandbox** de Twilio.
3. **Configurar el webhook**: En **Twilio Console**, en **"When a message comes in"**, pon la URL de tu **servidor en Vercel** (por ejemplo: `https://chatbot-whatsapp-ijxu.vercel.app/whatsapp`).


### **Enlaces útiles**:

- **Repositorio GitHub**: [GitHub - FreestyleBot](https://github.com/tu_usuario/chatbot-whatsapp)
- **Documentación de Twilio**: [Twilio API Docs](https://www.twilio.com/docs)
- **Documentación de Flask**: [Flask Docs](https://flask.palletsprojects.com/)
- **Vercel**: [Vercel Docs](https://vercel.com/docs)





