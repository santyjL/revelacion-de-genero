"""Shared vintage ornaments."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.styles.theme import COLORS


def flourish() -> rx.Component:
    return rx.el.hr(class_name="ornament-line")


def corners() -> rx.Component:
    return rx.fragment(
        rx.el.span(class_name="corner-flourish tl"),
        rx.el.span(class_name="corner-flourish tr"),
        rx.el.span(class_name="corner-flourish bl"),
        rx.el.span(class_name="corner-flourish br"),
    )


def tiny_icon(symbol: str, class_name: str = "float-soft") -> rx.Component:
    return rx.text(
        symbol,
        font_size="1.6rem",
        class_name=class_name,
        color=COLORS["gold"],
        aria_hidden="true",
    )
