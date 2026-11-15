"""Reflex application entrypoint."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.pages.home import home_page
from revelacion_de_genero.styles.style import BASE_STYLE, STYLESHEETS

app = rx.App(
    style=BASE_STYLE,
    stylesheets=STYLESHEETS,
    html_lang="es",
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", custom_attrs={"crossorigin": "anonymous"}),
    ],
)

app.add_page(
    home_page,
    route="/",
    title="Revelación de género",
    description="Invitación digital para descubrir juntos si llega un niño o una niña.",
)
