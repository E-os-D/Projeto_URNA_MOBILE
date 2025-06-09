import flet as ft

def home_view():
    return ft.View(
        route="/",
        controls=[
            ft.Stack(
                controls=[
                    # Quadrado preto (fundo deslocado)
                    ft.Container(
                        width=1200,
                        height=900,
                        bgcolor="black",
                        border_radius=5,
                        margin=ft.Margin(10, 10, 0, 0),  
                    ),
                    # Quadrado branco (sobreposição centralizada)
                    ft.Container(
                        width=350,
                        height=500,
                        bgcolor="white",
                        border_radius=5,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            [
                                ft.Image(src="/mnt/data/645d4cf4-2632-4c1a-abf5-f3c5d21aed69.png", width=100),
                                ft.Text("Urna", size=30, weight="bold"),
                                ft.Text("Eletrônica", size=30, weight="bold"),
                                ft.TextButton("Votar", on_click=lambda _: _.page.go("/votacao_presidente")),
                                ft.Row(
                                    [
                                        ft.Text("→ Administrador."),
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                    ),
                ],
                expand=True,
                alignment=ft.alignment.center,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )