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

Las respuestas del formulario se guardan en `data/attendance.csv`. Ese archivo no se sirve como estático.
Las invitaciones familiares guardan una fila por integrante con un `invitation_id` compartido; se permiten de 2 a 6 integrantes contando a quien responde. Los reportes cuentan personas, no invitaciones.

## Reporte diario por Gmail

1. Copia `.env.example` a `.env` y completa remitente, destinatario y rutas OAuth.
2. Coloca `credentials/client_secret.json` (no se versiona).
3. La primera ejecución de `python -m scripts.send_daily_report` abre el flujo OAuth y guarda `credentials/token.json`.
4. Programa cron en `America/Managua` hasta el 22 de noviembre de 2026:

```cron
0 20 * * * cd /ruta/al/proyecto && .venv/bin/python -m scripts.send_daily_report
```

Los envíos exitosos quedan en `data/email_log.json`. Un fallo no borra el CSV y se puede reintentar.

## Tests

```bash
pytest
```
