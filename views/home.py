import flet as ft

window_width = 950  # valor padrão inicial

def home_view(page: ft.Page):

    def on_resize(e):
        global window_width
        window_width = e.window_width
        img.width = get_responsive_image_width()
        page.update()

    def get_responsive_image_width():
        largura = window_width
        if largura > 950:
            largura = 950
        elif largura < 300:
            largura = 300
        return largura * 0.34

    img = ft.Image(
        src="img/Home.png",
        width=get_responsive_image_width(),
        fit=ft.ImageFit.CONTAIN,
    )

    page.on_resize = on_resize

    return ft.View(
        route="/",
        bgcolor="#FCF8EC",
        padding=20,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            expand=True,
                            alignment=ft.alignment.center,
                            content=ft.ResponsiveRow(
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        col={"sm": 12, "md": 10, "lg": 8, "xl": 6},
                                        padding=40,
                                        bgcolor="white",
                                        border=ft.border.all(width=1, color="black"),
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=0,
                                            color="black",
                                            offset=ft.Offset(15, 15),
                                        ),
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            scroll=ft.ScrollMode.AUTO,
                                            spacing=20,
                                            controls=[
                                                ft.Text("Urna", size=60),
                                                ft.Text("Eletrônica", size=60),
                                                img,
                                                ft.TextButton(
                                                    "Votar.",
                                                    on_click=lambda e: e.page.go("/eleitor_login"),
                                                    style=ft.ButtonStyle(color="black"),
                                                ),
                                                ft.Container(height=10),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.TextButton(
                                                            "→ Administrador.",
                                                            on_click=lambda e: e.page.go("/admin_login"),
                                                            style=ft.ButtonStyle(color="black"),
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                    )
                                ]
                            ),
                        )
                    ],
                ),
            )
        ],
    )
