import flet as ft

def home_view():
    return ft.View(
        route="/",
        bgcolor = "#FCF8EC",
        controls=[
            ft.Stack(
                controls=[
                    # Quadrado preto (fundo deslocado)
                    ft.Container(
                        width=1700,
                        height=840,
                        bgcolor="black",
                        margin=ft.Margin(70, 70, 0, 0),  
                    ),
                    # Quadrado branco (sobreposição centralizada)
                    ft.Container(
                        width=1700,
                        height=850,
                        bgcolor="white",
                        border=ft.border.all(width=1, color="black"),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                # Conteúdo principal centralizado
                                ft.Column(
                                    controls=[
                                        ft.Image(src="/mnt/data/645d4cf4-2632-4c1a-abf5-f3c5d21aed69.png", width=100),
                                        ft.Text("Urna", size=30, weight="bold"),
                                        ft.Text("Eletrônica", size=30, weight="bold"),
                                        ft.TextButton("Votar", on_click=lambda e: e.page.go("/votacao_presidente")),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True
                                ),

                                # Botão do administrador na base
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            "→ Administrador",
                                            on_click=lambda e: e.page.go("/admin_login"),
                                            style=ft.ButtonStyle(
                                                color="black",
                                                overlay_color="transparent"
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
                expand=True,
                alignment=ft.alignment.center,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )