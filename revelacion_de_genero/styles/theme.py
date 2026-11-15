"""Visual tokens for the vintage gender-reveal invitation."""

from __future__ import annotations

COLORS = {
    "ivory": "#F4EBDD",
    "cream": "#E8D9C3",
    "brown": "#705744",
    "sepia": "#46352C",
    "rose": "#C8798C",
    "blue": "#83B8D2",
    "muted_pink": "#F0BCC7",
    "sage": "#A6AA91",
    "gold": "#B69A6B",
    "paper": "#FBF6EE",
    "white": "#FFFDF8",
}

FONTS = {
    "serif": '"Playfair Display", "Cormorant Garamond", "Times New Roman", serif',
    "display": '"Cormorant Garamond", "Playfair Display", Georgia, serif',
    "script": '"Great Vibes", "Palatino Linotype", cursive',
    "body": '"Lora", Georgia, serif',
    "sans": '"Lato", "Segoe UI", sans-serif',
}

SPACE = {
    "xs": "0.35rem",
    "sm": "0.75rem",
    "md": "1.25rem",
    "lg": "2rem",
    "xl": "3rem",
    "section": "clamp(2.5rem, 8vw, 4.5rem)",
}

RADIUS = {
    "card": "1.15rem",
    "soft": "0.85rem",
    "pill": "999px",
}

SHADOWS = {
    "paper": "0 0.85rem 1.8rem rgba(70, 53, 44, 0.12)",
    "soft": "0 0.4rem 1.1rem rgba(70, 53, 44, 0.1)",
}

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&"
    "family=Great+Vibes&"
    "family=Lato:ital,wght@0,400;0,700;1,400&"
    "family=Lora:ital,wght@0,400;0,500;1,400&"
    "family=Playfair+Display:ital,wght@0,600;0,700;1,600&"
    "display=swap"
)
