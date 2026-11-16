
import reflex as rx

config = rx.Config(
    app_name="revelacion_de_genero",

    show_built_with_reflex=False,

    # Dirección pública del backend
    api_url="https://revelacion-de-genero-production.up.railway.app",

    # Dirección pública del frontend
    deploy_url="https://revelacion-de-genero-public.vercel.app",

    plugins=[
        rx.plugins.SitemapPlugin(),

        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="light",
                has_background=False,
                radius="large",
                accent_color="brown",
                gray_color="sand",
            )
        ),
    ],
)
