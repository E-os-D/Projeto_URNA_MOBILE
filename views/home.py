import flet as ft

def home_view():
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
                    scroll=ft.ScrollMode.AUTO,  # ← SCROLL AQUI
                    controls=[
                        ft.Container(
                            width=950,
                            padding=10,
                            bgcolor="white",
                            border=ft.border.all(width=1, color="black"),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=0,
                                color="black",
                                offset=ft.Offset(15, 15)
                            ),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.AUTO,  # ← E AQUI DENTRO TAMBÉM
                                controls=[
                                    ft.Text("Urna", size=60),
                                    ft.Text("Eletrônica", size=60),

                                    ft.Image(src="img/Home.png", width=320),

                                    ft.TextButton(
                                        "Votar.",
                                        on_click=lambda e: e.page.go("/eleitor_login"),
                                        style=ft.ButtonStyle(color="black")
                                    ),

                                    ft.Container(height=10),

                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.TextButton(
                                                "→ Administrador.",
                                                on_click=lambda e: e.page.go("/admin_login"),
                                                style=ft.ButtonStyle(color="black")
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ],
    )
