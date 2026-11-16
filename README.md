# Revelación de género

Invitación digital vintage construida con **Reflex 0.11.0**. La interfaz está pensada primero para móvil, con medidas relativas (`rem`, `%`, `clamp`) y el sistema visual en `revelacion_de_genero/styles/style.py` más `assets/style.css` (tipografías, textura y animaciones).

## Cómo ejecutar

```bash
source .venv/bin/activate
pip install -r requirements.txt
reflex run
```

Coloca la fotografía en `assets/baby_photo.jpg` cuando la tengas. El versículo bíblico se configura en `.env` (`BIBLE_VERSE_TEXT` y `BIBLE_VERSE_REFERENCE`) para no inventar el texto.

## Confirmaciones

Las respuestas del formulario se guardan en `data/attendance.csv` dentro del servidor. Ese archivo no se sirve como estático. En contenedores, monta un volumen persistente en `data/` (o configura `ATTENDANCE_CSV`) para que los datos sobrevivan a reinicios y nuevos despliegues.
Las invitaciones familiares guardan una fila por integrante con un `invitation_id` compartido; se permiten de 2 a 6 integrantes contando a quien responde. Los reportes cuentan personas, no invitaciones.

Después de guardar correctamente una respuesta, la aplicación envía en segundo plano un correo a los organizadores con el CSV completo actualizado, tanto para respuestas afirmativas como negativas. Si el correo falla, el RSVP permanece guardado y la interfaz lo informa.

## Envío de correo y reporte diario

La opción recomendada para producción es SMTP con TLS, porque no requiere archivos OAuth dentro de la imagen. Se puede usar con un servidor propio de código abierto como Mailu, Mailcow o Postal, o con cualquier relay SMTP compatible. Configura en el entorno de producción:

```env
EMAIL_TRANSPORT=smtp
EMAIL_SENDER=organizador@example.com
EMAIL_RECIPIENT=destino@example.com
SMTP_HOST=mail.example.com
SMTP_PORT=587
SMTP_SECURITY=starttls
SMTP_USERNAME=usuario-smtp
SMTP_PASSWORD=secreto-smtp
ATTENDANCE_CSV=/revelacion_de_genero/data/attendance.csv
EMAIL_LOG_PATH=/revelacion_de_genero/data/email_log.json
```

Para un servidor SMTP con SSL implícito (normalmente puerto 465), usa `SMTP_SECURITY=ssl`. No uses conexiones SMTP sin cifrar. Guarda las credenciales como secretos del proveedor de despliegue; no las añadas a Git ni a la imagen. Si se usa un servidor autohospedado, configura también DNS y reputación del dominio (SPF, DKIM y DMARC) para mejorar la entrega.

Gmail API sigue disponible como alternativa. Configura `EMAIL_TRANSPORT=gmail`, `GMAIL_SENDER`, `GMAIL_RECIPIENT`, `GOOGLE_CLIENT_SECRET_FILE` y `GOOGLE_TOKEN_FILE`. Autoriza la cuenta una sola vez en un equipo con navegador mediante `python -m scripts.authorize_gmail`, y provisiona el token OAuth como secreto persistente en producción. El error `Missing Google OAuth client secret file` significa que el contenedor no encuentra el archivo de credenciales en la ruta configurada; el archivo local del repositorio no se incluye en la imagen por seguridad.

El ejemplo completo de variables está en [.env.example](./.env.example). Nunca copies el `.env`, el CSV o los secretos OAuth dentro de la imagen.

Programa los reportes diarios en `America/Managua` hasta el 22 de noviembre de 2026. El mismo transporte (SMTP o Gmail API) se usa para los avisos inmediatos y para el reporte diario:

```cron
0 20 * * * cd /ruta/al/proyecto && .venv/bin/python -m scripts.send_daily_report
```

Los envíos exitosos quedan en `data/email_log.json`. Un fallo no borra el CSV y se puede reintentar.

## Tests

```bash
pytest
```
