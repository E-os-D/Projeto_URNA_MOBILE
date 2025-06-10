import flet as ft

def home_view():
    return ft.View(
        route="/",
        bgcolor="#FCF8EC",
        controls=[
            ft.Stack(
                controls=[
                    # Fundo preto deslocado
                    ft.Container(
                        width=1700,
                        height=840,
                        bgcolor="black",
                        margin=ft.Margin(70, 70, 0, 0),
                    ),
                    # Fundo branco por cima
                    ft.Container(
                        width=1700,
                        height=850,
                        bgcolor="white",
                        border=ft.border.all(width=1, color="black"),
                        content=ft.Column(
                            controls=[
                                # Linha com imagem e texto
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        # Coluna com imagem e botão
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Image(src="img/imgHome.png", width=200),
                                                ft.TextButton(
                                                    "Votar.",
                                                    on_click=lambda e: e.page.go("/votacao_presidente"),
                                                    style=ft.ButtonStyle(
                                                        color="black",
                                                        overlay_color="transparent"
                                                    )
                                                ),
                                            ]
                                        ),
                                       # Coluna com título
                                        ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                            controls=[
                                                ft.Text("Urna", size=40, weight="bold"),
                                                ft.Text("Eletrônica", size=40, weight="bold"),
                                            ]
                                        )
                                    ]
                                ),
                                # Botão do administrador
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            "→ Administrador.",
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
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
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