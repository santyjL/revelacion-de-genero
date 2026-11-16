"""Landing page that opens the existing invitation."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish


def landing_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Revelación de género", as_="h1", class_name="landing-title"),
            rx.text("Un hermoso bebé viene en camino", class_name="landing-subtitle"),
            rx.box(
                rx.link(
                    rx.image(
                        src=rx.asset("decorations/carta.png"),
                        alt="Carta de invitación; toca para abrirla",
                        class_name="landing-letter",
                    ),
                    href="/invitacion",
                    aria_label="Abrir la invitación",
                    class_name="landing-letter-link",
                ),
                rx.image(
                    src=rx.asset("decorations/osita.png"),
                    alt="Osita decorativa en la esquina superior izquierda",
                    class_name="landing-bear landing-bear-girl",
                    width="10rem",
                    height="10rem",
                    position="absolute",
                    top="-50px",
                ),
                rx.image(
                    src=rx.asset("decorations/oso-niño.png"),
                    alt="Osito decorativo en la esquina inferior derecha",
                    class_name="landing-bear landing-bear-boy",
                    width="10rem",
                    height="10rem",
                    position="absolute",
                    right="-50px"
                ),
                class_name="landing-card-scene",
            ),
            rx.box("",
                   margin="0.5rem",),
            flourish(),
            rx.text(
                "Toca la carta para abrir la invitación",
                class_name="landing-instruction",
            ),
            align="center",
            spacing="0",
            width="100%",
        ),
        class_name="landing-page",
    )
