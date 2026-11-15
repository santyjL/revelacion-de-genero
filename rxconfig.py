import reflex as rx

config = rx.Config(
    app_name="revelacion_de_genero",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
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