import flet as ft

def admin_painel_view():
    def voltar(e):
        e.page.go("/")

    def ir_candidatos(e):
        e.page.go("/cadastro_candidato_painel")

    def ir_relatorio(e):
        e.page.go("/resultado")

    def ir_grafico(e):
        e.page.go("/graficos")

    def ir_admin(e):
        e.page.go("/cadastro_admin")

    # Linha 1 de ícones
    opcoes = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_candidatos.png", width=150),
                    ft.Container(
                        content=ft.Text("Candidatos.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_candidatos
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_relatorio.png", width=150),
                    ft.Container(
                        content=ft.Text("Relatório.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_relatorio
            )
        ],
        alignment="center",
        spacing=80
    )

    # Linha 2 de ícones
    opcoes2 = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_grafico.png", width=150),
                    ft.Container(
                        content=ft.Text("Gráfico.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_grafico
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_administrador.png", width=150),
                    ft.Container(
                        content=ft.Text("Administrador.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_admin
            )
        ],
        alignment="center",
        spacing=80
    )

    # Botão de voltar no canto inferior direito
    voltar_row = ft.Row(
        [ft.TextButton(
            "← Voltar",
            on_click=voltar,
            style=ft.ButtonStyle(color="black")
        )],
        alignment="end"
    )

    return ft.View(
        route="/admin_painel",
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
                                        padding=70,
                                        bgcolor="white",
                                        border=ft.border.all(width=1, color="black"),
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=0,
                                            color="black",
                                            offset=ft.Offset(15, 15)
                                        ),
                                        content=ft.Column(
                                            scroll=ft.ScrollMode.AUTO,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                            ft.Container(  # Centro dos ícones
                                                content=ft.Column(
                                                    [opcoes, opcoes2],
                                                    spacing=50,
                                                    alignment="center"
                                                ),
                                                expand=True,
                                                alignment=ft.alignment.center
                                            ),
                                            voltar_row  # Botão no fim
                                        ],
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )