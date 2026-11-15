"""Dedicated design system: layout, type, component styles and stylesheet wiring."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.styles.animations import FADE_UP, FLOAT, PULSE, SHIMMER
from revelacion_de_genero.styles.theme import COLORS, FONTS, GOOGLE_FONTS, RADIUS, SHADOWS, SPACE

STYLESHEETS = [
    GOOGLE_FONTS,
    "/style.css",
]


def _bp(**values: str) -> rx.breakpoints:
    return rx.breakpoints(**values)


PAGE = {
    "width": "100%",
    "min_height": "100dvh",
    "background_color": COLORS["ivory"],
    "background_image": "var(--paper-texture)",
    "color": COLORS["brown"],
    "font_family": FONTS["body"],
    "font_size": "clamp(1.08rem, 2.8vw, 1.2rem)",
    "line_height": "1.65",
    "overflow_x": "hidden",
}

SHELL = {
    "width": "min(100%, 42rem)",
    "margin_left": "auto",
    "margin_right": "auto",
    "padding_inline": _bp(initial="1.1rem", sm="1.6rem", md="2rem"),
    "padding_bottom": SPACE["xl"],
}

SECTION = {
    "width": "100%",
    "padding_block": SPACE["section"],
    "align_items": "center",
    "text_align": "center",
    "gap": SPACE["md"],
}

CARD = {
    "width": "100%",
    "background_color": COLORS["cream"],
    "background_image": "linear-gradient(180deg, rgba(255,253,248,0.55), rgba(232,217,195,0.9))",
    "border": f"1px solid {COLORS['gold']}",
    "border_radius": RADIUS["card"],
    "box_shadow": SHADOWS["paper"],
    "padding": _bp(initial="1.25rem", sm="1.7rem"),
    "position": "relative",
}

PANEL = {
    **CARD,
    "background_color": COLORS["paper"],
    "box_shadow": f"inset 0 0 0 0.35rem {COLORS['cream']}, {SHADOWS['paper']}",
}

HEADING = {
    "font_family": FONTS["serif"],
    "color": COLORS["sepia"],
    "letter_spacing": "0.04em",
    "line_height": "1.2",
    "font_weight": "700",
    "text_wrap": "balance",
}

SCRIPT = {
    "font_family": FONTS["script"],
    "color": COLORS["gold"],
    "font_weight": "400",
    "line_height": "1.3",
}

BODY_TEXT = {
    "font_family": FONTS["body"],
    "color": COLORS["brown"],
    "max_width": "36rem",
}

LABEL = {
    "font_family": FONTS["sans"],
    "font_size": "1rem",
    "font_weight": "700",
    "letter_spacing": "0.08em",
    "text_transform": "uppercase",
    "color": COLORS["sepia"],
}

INPUT = {
    "width": "100%",
    "min_height": "2.85rem",
    "border_radius": RADIUS["soft"],
    "border": f"1px solid {COLORS['gold']}",
    "background_color": COLORS["white"],
    "color": COLORS["sepia"],
    "font_family": FONTS["sans"],
    "font_size": "1rem",
    "padding_inline": "0.95rem",
}

BUTTON = {
    "width": "100%",
    "min_height": "3rem",
    "border_radius": RADIUS["pill"],
    "background_color": COLORS["sepia"],
    "color": COLORS["ivory"],
    "font_family": FONTS["sans"],
    "font_weight": "700",
    "letter_spacing": "0.12em",
    "text_transform": "uppercase",
    "font_size": "0.94rem",
    "box_shadow": SHADOWS["soft"],
    "cursor": "pointer",
    "_hover": {"background_color": COLORS["brown"]},
}

OPTION_CARD = {
    "width": "100%",
    "min_height": "3.2rem",
    "padding": "0.9rem 1rem",
    "border_radius": RADIUS["soft"],
    "border": f"1px solid {COLORS['gold']}",
    "background_color": COLORS["white"],
    "font_family": FONTS["sans"],
    "font_size": "1.05rem",
    "text_align": "left",
    "cursor": "pointer",
    "color": COLORS["sepia"],
}

PHOTO_FRAME = {
    "width": "min(86vw, 27rem)",
    "padding": "0.7rem",
    "background": f"linear-gradient(135deg, {COLORS['gold']}, {COLORS['cream']}, {COLORS['gold']})",
    "border_radius": "0.4rem",
    "box_shadow": SHADOWS["paper"],
}

ULTRASOUND_VIDEO = {
    "display": "block",
    "width": "100%",
    "height": "auto",
    "aspect_ratio": "4 / 3",
    "object_fit": "contain",
    "background_color": COLORS["sepia"],
    "border_radius": "0.2rem",
}

COUNT_CELL = {
    "flex": "1",
    "min_width": "22%",
    "padding_block": "0.75rem",
    "background_color": "#ffffff33",
    "border-top": f"1px solid {COLORS['gold']}",
    "border_radius": RADIUS["soft"],
    "box_shadow": SHADOWS["soft"],
}

TEAM_BOY = {
    **CARD,
    "background_image": f"linear-gradient(180deg, {COLORS['white']}, {COLORS['blue']})",
    "border": f"1px solid {COLORS['blue']}",
}

TEAM_GIRL = {
    **CARD,
    "background_image": f"linear-gradient(180deg, {COLORS['white']}, {COLORS['muted_pink']})",
    "border": f"1px solid {COLORS['rose']}",
}

BASE_STYLE = {
    "font_family": FONTS["body"],
    "color": COLORS["brown"],
    "background_color": COLORS["ivory"],
    rx.heading: HEADING,
    rx.text: {"color": COLORS["brown"]},
    rx.button: {
        "font_family": FONTS["sans"],
    },
    rx.input: INPUT,
    "::selection": {
        "background_color": COLORS["muted_pink"],
        "color": COLORS["sepia"],
    },
    ".invite-shell": SHELL,
    ".invite-section": SECTION,
    ".invite-card": CARD,
    ".invite-panel": PANEL,
    ".script-text": SCRIPT,
    ".serif-title": HEADING,
    ".body-copy": BODY_TEXT,
    ".field-label": LABEL,
    ".option-card": OPTION_CARD,
    ".option-card.selected": {
        "border": f"2px solid {COLORS['sepia']}",
        "background_color": COLORS["cream"],
        "box_shadow": SHADOWS["soft"],
    },
    ".photo-frame": PHOTO_FRAME,
    ".ultrasound-video": ULTRASOUND_VIDEO,
    ".count-cell": COUNT_CELL,
    ".team-boy": TEAM_BOY,
    ".team-girl": TEAM_GIRL,
    ".cta-button": BUTTON,
    f".{FADE_UP}": {
        "animation": "fadeUp 0.9s ease both",
    },
    f".{FLOAT}": {
        "animation": "floatSoft 5.5s ease-in-out infinite",
    },
    f".{PULSE}": {
        "animation": "pulseSoft 2.8s ease-in-out infinite",
    },
    f".{SHIMMER}": {
        "background": f"linear-gradient(90deg, {COLORS['gold']}, {COLORS['cream']}, {COLORS['gold']})",
        "background_size": "200% 100%",
        "animation": "goldShimmer 6s linear infinite",
    },
}
