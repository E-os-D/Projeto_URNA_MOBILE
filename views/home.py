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
                        padding=20, # Adicionar um preenchimento é bom para o visual
                        # MUDANÇA PRINCIPAL: Usar Column em vez de Stack aqui
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                # Este Container vai ocupar todo o espaço vertical disponível,
                                # centralizando seu conteúdo e empurrando o botão de admin para baixo.
                                ft.Container(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Column(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                                controls=[
                                                    ft.Image(src="img/Home.png", width=400),
                                                    ft.TextButton(
                                                        "Votar.",
                                                        on_click=lambda e: e.page.go("/eleitor_login"),
                                                        style=ft.ButtonStyle(
                                                            color="black"
                                                        )
                                                    ),
                                                ]
                                            ),
                                            ft.Column(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                                controls=[
                                                    ft.Text("Urna", size=80),
                                                    ft.Text("Eletrônica", size=80, weight=None),
                                                ]
                                            )
                                        ]
                                    )
                                ),
                                # Botão do administrador no final da coluna, alinhado à direita
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.TextButton(
                                            "→ Administrador.",
                                            on_click=lambda e: e.page.go("/admin_login"),
                                            style=ft.ButtonStyle(
                                                color="black"
                                            )
                                        )
                                    ]
                                )
                            ]
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