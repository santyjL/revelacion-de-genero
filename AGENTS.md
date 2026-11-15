<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** — up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above — do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs — components, state management, events, styling, database, routing, authentication — use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available — always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->


# AGENT.md — Gender Reveal Invitation & RSVP

## 1. Project Overview

Develop an elegant, responsive and interactive digital invitation website for a Gender Reveal celebration using **Python 3.11+ and Reflex 0.11.0**.

The application must function as a digital invitation card where guests can:

1. Read the invitation and event details.
2. View a photograph of the expected baby.
3. Discover the two teams: Team Niño and Team Niña.
4. See a live countdown to the celebration.
5. Submit their attendance confirmation through an RSVP form.

All attendance records must be stored persistently in a CSV file. The system must automatically send a daily CSV report to a designated Gmail address until November 22, 2026.

The project must prioritize clean architecture, modularity, readability, maintainability, security and responsive design.

### Main objectives

- Create a visually attractive vintage-inspired invitation.
- Deliver an intuitive mobile-first experience.
- Make attendance confirmation simple.
- Persist attendance records without losing information.
- Automate daily email reports.
- Keep the countdown synchronized with the event date.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Main programming language |
| Reflex 0.11.0 | Full-stack web framework |
| HTML/CSS | Custom visual presentation |
| CSV | Persistent attendance storage |
| Python `csv` | Reading and writing records |
| Gmail API | Automated email delivery |
| Google OAuth 2.0 | Secure Gmail authentication |
| `zoneinfo` | Nicaragua timezone management |
| `pytest` | Automated testing |
| APScheduler or system cron | Scheduled reporting, if appropriate |

### Dependency requirements

Pin the framework version:

```txt
reflex==0.11.0
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
python-dotenv
pytest
```

Add dependencies only when they are actually needed.

Use Python's standard library whenever possible.

---

## 3. Project Architecture

Organize the application into independent modules.

```text
gender_reveal/
│
├── assets/
│   ├── baby_photo.jpg
│   ├── decorations/
│   └── icons/
│
├── gender_reveal/
│   ├── __init__.py
│   ├── gender_reveal.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── hero.py
│   │   ├── invitation.py
│   │   ├── baby_photo.py
│   │   ├── team_cards.py
│   │   ├── event_details.py
│   │   ├── countdown.py
│   │   └── rsvp_form.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   └── home.py
│   │
│   ├── state/
│   │   ├── __init__.py
│   │   └── rsvp_state.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── csv_service.py
│   │   ├── email_service.py
│   │   └── validation_service.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   └── styles/
│       ├── __init__.py
│       └── theme.py
│
├── scripts/
│   └── send_daily_report.py
│
├── data/
│   ├── attendance.csv
│   └── email_log.json
│
├── credentials/
│   └── .gitkeep
│
├── tests/
│   ├── test_csv_service.py
│   ├── test_validation.py
│   └── test_email_service.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── rxconfig.py
├── README.md
└── AGENT.md
```

### Architecture principles

- `components/`: Contains reusable visual components.
- `pages/`: Defines application pages and assembles components.
- `state/`: Manages Reflex state and frontend events.
- `services/`: Contains business logic and external integrations.
- `config/`: Centralizes application configuration.
- `styles/`: Defines reusable colors, typography and styling constants.
- `scripts/`: Contains independent executable processes.
- `data/`: Stores application records.
- `tests/`: Validates application functionality.

Avoid placing the entire application inside a single Python file.

Each module should have one clearly defined responsibility.

Use explicit imports and avoid circular dependencies.

---

## 4. Visual Identity and Design System

### Main aesthetic: Vintage Gender Reveal

The website should resemble an elegant vintage baby announcement, combining nostalgic decorative elements with a modern and polished interface.

The design should communicate tenderness, anticipation and family celebration.

**The dominant visual language must be vintage, not a conventional modern baby shower template.**

### Color palette

Use a balanced combination of warm neutral tones, powder blue and dusty pink.

| Color | HEX | Application |
|---|---|---|
| Antique Ivory | `#F4EBDD` | Main background |
| Warm Cream | `#E8D9C3` | Cards and sections |
| Vintage Brown | `#705744` | Main typography |
| Dark Sepia | `#46352C` | Headings |
| Dusty Rose | `#D9A1A5` | Team Niña |
| Powder Blue | `#A9C9D8` | Team Niño |
| Muted Pink | `#EBC6C8` | Decorative details |
| Sage Green | `#A6AA91` | Secondary decoration |
| Antique Gold | `#B69A6B` | Borders and accents |

### Typography

Combine three typography styles:

- **Serif:** Main headings and important announcements.
- **Handwritten/script:** Decorative phrases and personal touches.
- **Sans-serif:** Form labels, buttons and functional information.

Suggested font families:

- Playfair Display
- Cormorant Garamond
- Great Vibes
- Lora
- Lato

Load fonts efficiently and provide fallback fonts.

### Decorative elements

Use subtle visual elements:

- Vintage paper texture.
- Fine ornamental borders.
- Small flowers and botanical illustrations.
- Teddy bears.
- Baby-themed illustrations.
- Delicate ribbons.
- Vintage frames around photographs.
- Subtle shadows and rounded corners.

Avoid excessive decoration that competes with the invitation text.

Use restrained animations and respect reduced-motion preferences.

---

## 5. Website Structure and Content

Build the application as a single-page invitation with a vertical layout.

The entire experience should feel like reading an elegant physical invitation.

### Section 1 — Hero

Display the main announcement:

**¡UNA GRAN SORPRESA ESTÁ POR LLEGAR! 🧸🩷🩵**

Use a large serif heading, centered composition and decorative vintage elements.

Include the introductory text:

"Agradecemos a Dios por este milagro que llena nuestro hogar de ilusión.

Un corazón pequeñito crece dentro de mami y se alimenta del amor de papi.

Con muchísimo amor y emoción queremos invitarte a compartir un momento muy especial con nosotros."

### Section 2 — Baby photograph

Create a dedicated photograph section.

Requirements:

- Use a centered photograph.
- Place the image inside an elegant vintage frame.
- Add decorative elements around the image.
- Preserve the original aspect ratio.
- Make the image responsive.

Use the following asset:

```text
assets/baby_photo.jpg
```

If the photograph is not available, show a temporary decorative placeholder.

Below the photograph, include a configurable Bible verse.

**Important:** Do not invent the Bible verse. Keep its text configurable until the exact verse and reference are provided.

### Section 3 — The big reveal

Display:

**¡Estamos a punto de descubrir si nuestro pequeño milagro será NIÑA o NIÑO!**

"Un día lleno de alegría, amor y mucha ilusión nos espera."

Follow with:

**¿NOS ACOMPAÑAS A DESCUBRIRLO?**

Use an elegant visual transition to introduce the two teams.

### Section 4 — Team selection

Title:

**¡Elige tu equipo!**

Create two visually balanced cards.

#### TEAM NIÑO

Use powder blue as the dominant accent.

Text:

"Si crees que será niño:

Ven con una prenda en tono celeste y trae pañitos húmedos."

Decorate with subtle blue ribbons, stars or teddy bear illustrations.

#### TEAM NIÑA

Use dusty pink as the dominant accent.

Text:

"Si crees que será niña:

Ven con una prenda en tono rosado y trae pañales Huggies Dermacare o Pampers talla P, M o G en adelante."

Decorate with subtle pink ribbons, flowers or teddy bear illustrations.

Below the cards, display:

"¡Elige tu equipo, ven preparado y acompáñanos a descubrir si acertaste!"

The cards must be visually distinct without breaking the overall vintage aesthetic.

### Section 5 — Event details

Present the event information inside a decorative invitation panel.

**Fecha:** 29 de noviembre de 2026

**Hora:** 3:00 PM

**Lugar:** Restaurante Pikito's

Use appropriate icons and a clear visual hierarchy.

Do not invent an address for the restaurant.

### Section 6 — Countdown

Display:

**¡ACTIVA LA CUENTA REGRESIVA Y PREPÁRATE PARA LA SORPRESA!**

Create a live countdown with four units:

- Days
- Hours
- Minutes
- Seconds

Target:

```text
2026-11-29 15:00:00
Timezone: America/Managua
```

Requirements:

1. The countdown must update every second.
2. It must use the visitor's current synchronized event deadline.
3. It must not rely on the browser's local timezone.
4. It must handle negative or expired countdown values.
5. When the event begins, replace the countdown with a celebratory message.
6. Keep the countdown visually consistent with the vintage design.

Implement the countdown efficiently.

Prefer a lightweight client-side timer rather than sending a Reflex backend event every second.

The deadline must be configurable in the application settings.

### Section 7 — RSVP confirmation

Title:

**CONFIRMAR ASISTENCIA 🩷🩵**

Introduction:

"¡Queremos contar contigo en este día tan especial!"

Create an elegant form containing:

**Field 1 — Your name**

Label:

"Tu nombre"

Input:

- Required.
- Text input.
- Remove leading and trailing whitespace.
- Minimum 2 characters.
- Maximum 100 characters.

**Field 2 — Attendance confirmation**

Question:

"¿Podrás asistir?"

Options:

1. "¡Sí, claro! ¡No me lo pierdo!"
2. "Esta vez no voy a poder."

Use radio buttons or elegant selectable cards.

**Field 3 — Team selection**

Include an optional selection:

- TEAM NIÑO.
- TEAM NIÑA.
- Aún no lo sé.

This field is useful for organizing the celebration but must not be mandatory.

**Submit button**

Text:

"CONFIRMAR MI ASISTENCIA"

After submission:

- Validate the information.
- Save the record in the CSV file.
- Show a confirmation message.
- Prevent accidental duplicate submissions.
- Reset the form only after a successful save.

Display different confirmation messages depending on the selected attendance option.

Never show private administrative information to visitors.

### Section 8 — Footer

Display:

"Con cariño,

Los futuros papás. 🤍"

Use a delicate vintage closing composition.

---

## 6. CSV Data Management

The application must use a CSV file as its persistent attendance storage.

File:

```text
data/attendance.csv
```

### CSV structure

Use these columns:

```csv
id,name,attendance,team,submitted_at
```

Example:

```csv
1,María López,yes,girl,2026-11-14T18:30:00-06:00
2,Carlos Pérez,no,unknown,2026-11-14T19:15:00-06:00
```

### Implementation requirements

Implement CSV operations exclusively through `services/csv_service.py`.

Required functions:

```python
def initialize_csv() -> None:
    ...

def save_attendance(record: dict) -> bool:
    ...

def read_attendance() -> list[dict]:
    ...

def count_attendance() -> dict:
    ...

def export_attendance() -> str:
    ...
```

The CSV service must:

- Create the file automatically if it does not exist.
- Write headers only once.
- Append new records without deleting previous ones.
- Use UTF-8 encoding.
- Handle Spanish characters correctly.
- Validate the expected fields.
- Handle file access errors.
- Protect against concurrent writes using an appropriate file-locking strategy.
- Avoid exposing the CSV file publicly through the frontend.

Use atomic file operations where appropriate.

Do not use a CSV file as a substitute for a relational database if the project later grows substantially.

---

## 7. Gmail Integration

The system must automatically send the attendance CSV to a designated Gmail address.

Use the official Gmail API with OAuth 2.0.

Implement the integration in:

```text
gender_reveal/services/email_service.py
```

### Email configuration

Use environment variables:

```env
GMAIL_SENDER=
GMAIL_RECIPIENT=
GOOGLE_CLIENT_SECRET_FILE=
GOOGLE_TOKEN_FILE=
```

The application must never contain hardcoded credentials.

Keep OAuth tokens and client credentials outside version control.

Use the Gmail API to create and send an email with the CSV attached.

### Email content

Subject:

```text
Gender Reveal - Reporte diario de confirmaciones
```

Body:

```text
Hola,

Adjunto encontrarás el reporte actualizado de confirmaciones
de asistencia para la revelación de género del 29 de noviembre.

El archivo contiene los registros recibidos hasta el momento.

Saludos.
```

Attachment:

```text
attendance.csv
```

### Report information

The report should include:

- Total de confirmaciones.
- Personas que asistirán.
- Personas que no podrán asistir.
- Personas que aún no han confirmado no deben contabilizarse como respuestas negativas.
- Distribución por equipo.
- Fecha y hora de generación del reporte.

The CSV attachment must contain the complete current attendance records.

### Error handling

If Gmail delivery fails:

- Record the error.
- Do not delete or modify the CSV.
- Preserve the possibility of retrying.
- Do not mark an unsuccessful delivery as completed.

Never expose Gmail errors, OAuth tokens or credentials to public users.

---

## 8. Automated Daily Email Reporting

This is an independent process and must not depend on the user opening the website.

### Scheduling requirements

Event date:

```text
November 29, 2026
```

Final reporting date:

```text
November 22, 2026
```

Frequency:

```text
Once per day
```

Suggested execution time:

```text
20:00 America/Managua
```

The process must run daily, including November 22, and stop after successfully completing that final scheduled report.

### Recommended implementation

Create:

```text
scripts/send_daily_report.py
```

This script must:

1. Load application configuration.
2. Determine the current date in `America/Managua`.
3. Check whether the reporting period is still active.
4. Read the complete CSV.
5. Generate report statistics.
6. Prepare the email.
7. Attach the CSV.
8. Send the email through Gmail.
9. Register successful delivery.
10. Log errors if delivery fails.

### Duplicate prevention

Use:

```text
data/email_log.json
```

Store information such as:

```json
{
  "2026-11-14": {
    "status": "sent",
    "sent_at": "2026-11-14T20:00:00-06:00"
  }
}
```

Before sending, verify that the date has not already been successfully processed.

A failed attempt must remain eligible for retry.

### Scheduling strategy

Prefer an external scheduler such as system cron or a hosting provider's scheduled jobs.

Example Linux cron configuration:

```cron
0 20 * * * cd /path/to/gender_reveal && /path/to/venv/bin/python -m scripts.send_daily_report
```

Configure the scheduler in the `America/Managua` timezone.

The scheduler must stop executing after November 22, 2026, or the script must safely exit without sending further reports.

**Important:** Reflex background events are not a durable job queue. Do not use a page-load event or an in-memory background loop as the only scheduling mechanism.

For local development, the script should also be executable manually for testing.

---

## 9. Reflex State Management

Implement the RSVP interaction in:

```text
gender_reveal/state/rsvp_state.py
```

Create an appropriate `rx.State` subclass.

Responsibilities:

- Manage form values.
- Validate submission.
- Execute the CSV storage service.
- Provide user feedback.
- Prevent repeated submissions while processing.

Use Reflex 0.11.0 conventions.

### Important version-specific considerations

- Pin Reflex to exactly `0.11.0`.
- Use `@rx.event` for event handlers.
- Avoid deprecated decorator stacking above `@rx.event`.
- Give form controls explicit identifiers and names.
- Use stable keys for dynamically rendered collections.
- Avoid blocking synchronous file or network operations in the event loop.
- Keep business logic outside the state class.

State classes should coordinate application behavior, not implement all the underlying services.

---

## 10. Security and Data Protection

Even though this is a small family invitation, implement basic security practices.

Requirements:

1. Validate all incoming form values on the backend.
2. Sanitize names before storage and display.
3. Protect against CSV formula injection when opening exported files in spreadsheet software.
4. Do not expose the CSV through a public static route.
5. Never expose Gmail credentials or OAuth tokens.
6. Use `.env` for configuration.
7. Include sensitive files in `.gitignore`.
8. Prevent spam submissions through appropriate rate limiting.
9. Prevent accidental duplicate submissions.
10. Keep administrative reporting separate from the public invitation.

Suggested `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/

credentials/*
!credentials/.gitkeep

data/attendance.csv
data/email_log.json

.reflex/
```

For production, store persistent data on a persistent volume or external storage. Do not assume that a deployment filesystem will preserve CSV changes across restarts or redeployments.

---

## 11. Responsive Design

The website must be mobile-first.

Prioritize:

- Smartphones.
- Tablets.
- Desktop screens.

### Mobile requirements

- Single-column layout.
- Comfortable typography.
- Large touch-friendly form controls.
- Two team cards stacked vertically when necessary.
- Countdown units that fit small screens.
- No horizontal overflow.
- Optimized images.

### Desktop requirements

- Centered invitation composition.
- Controlled maximum content width.
- Two team cards displayed side by side.
- Balanced spacing and typography.
- Elegant decorative backgrounds.

The website should look like a carefully designed digital invitation, not an administrative dashboard.

---

## 12. Performance and Code Quality

Follow Python best practices.

### Python standards

- Use type hints.
- Use descriptive variable and function names.
- Follow PEP 8.
- Use docstrings for public functions.
- Keep functions small and focused.
- Handle exceptions explicitly.
- Use `pathlib` for file paths.
- Use `datetime` and `zoneinfo` for dates.
- Avoid unnecessary global mutable state.
- Separate configuration from business logic.

### Code organization

Do not:

- Place all components in one file.
- Mix CSV operations with UI components.
- Mix Gmail operations with Reflex event handlers.
- Duplicate validation logic.
- Hardcode event dates in multiple modules.
- Put credentials in source code.
- Use unnecessary dependencies.

Create reusable functions and components.

---

## 13. Testing Requirements

Before considering the project complete, test the following.

### RSVP tests

- Submit a valid name.
- Submit an empty name.
- Submit a name containing Spanish characters.
- Submit both attendance options.
- Submit each team selection.
- Verify that records are saved correctly.

### CSV tests

- Initialize a missing CSV.
- Append multiple records.
- Read existing records.
- Preserve previous records.
- Handle invalid input.
- Verify UTF-8 compatibility.

### Email tests

- Generate the report.
- Verify CSV attachment.
- Test Gmail authentication errors.
- Test failed email delivery.
- Verify duplicate prevention.
- Verify that a successful delivery is registered.

Use mocks for Gmail tests instead of sending real emails.

### Countdown tests

- Verify the deadline.
- Verify the timezone.
- Verify the transition to zero.
- Verify behavior after the event begins.

### Scheduling tests

- Verify that reports are eligible before November 22.
- Verify that November 22 is included.
- Verify that November 23 and subsequent dates do not generate reports.
- Verify that a failed delivery can be retried.

---

## 14. Implementation Roadmap

Develop the application in the following order.

### Phase 1 — Project initialization

- Create the Reflex project.
- Pin dependencies.
- Establish the folder structure.
- Configure application settings.
- Define the design system.

### Phase 2 — Visual development

- Build the hero.
- Build the baby photograph section.
- Build the team cards.
- Build event details.
- Build the countdown.
- Build the footer.

First, ensure that the invitation looks complete before integrating backend functionality.

### Phase 3 — RSVP functionality

- Create the Reflex state.
- Implement form validation.
- Implement CSV storage.
- Connect the form to the storage service.
- Display confirmation messages.

### Phase 4 — Gmail integration

- Configure Google OAuth.
- Implement email generation.
- Attach the CSV.
- Implement report statistics.
- Test delivery.

### Phase 5 — Scheduling

- Implement the independent reporting script.
- Add duplicate protection.
- Configure the daily scheduler.
- Test the November 22 cutoff.

### Phase 6 — Final validation

- Test mobile and desktop.
- Verify all invitation text.
- Verify the countdown.
- Verify CSV persistence.
- Verify email delivery.
- Check security and configuration.
- Prepare deployment instructions.

---

## 15. Acceptance Criteria

The project is complete only when all the following conditions are met:

- [ ] The website runs using Reflex 0.11.0.
- [ ] The invitation displays all supplied text.
- [ ] The baby photograph can be displayed.
- [ ] The Bible verse is configurable.
- [ ] The two teams have distinct visual identities.
- [ ] Event information is correct.
- [ ] The countdown reaches November 29, 2026, at 3:00 PM Nicaragua time.
- [ ] The RSVP form accepts and validates submissions.
- [ ] Attendance information is saved in CSV.
- [ ] Existing records are preserved.
- [ ] Gmail can send the CSV report.
- [ ] Daily reports can execute independently of the website.
- [ ] Reports stop after November 22, 2026.
- [ ] Duplicate emails are prevented.
- [ ] Errors are logged.
- [ ] Credentials are protected.
- [ ] The interface is responsive.
- [ ] The code follows the defined modular architecture.

---

## 16. Instructions for the Coding Agent

Act as a senior Python developer and frontend engineer.

Your primary objective is to build a complete, maintainable and functional application rather than simply producing a visual mockup.

Follow these instructions:

1. Read the entire `AGENT.md` before writing code.
2. Respect the proposed architecture.
3. Implement functionality progressively.
4. Prioritize the visual quality of the invitation.
5. Keep Python code readable and modular.
6. Verify compatibility with Reflex 0.11.0.
7. Never invent missing personal information.
8. Do not invent the Bible verse.
9. Do not assume Gmail credentials exist.
10. Ask for missing configuration only when necessary.
11. Never replace persistent data during application initialization.
12. Test each service independently.
13. Document how to run the application and configure Gmail.
14. Do not declare the project complete until the acceptance criteria have been verified.

**Final design objective:** A beautiful, intimate and nostalgic digital invitation that feels like a vintage family announcement, while maintaining the reliability of a properly structured Python application.