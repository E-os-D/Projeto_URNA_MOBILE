import flet as ft

def admin_painel_view():
    def voltar(e):
        e.page.go("/")

    def ir_candidatos(e):
        e.page.go("/cadastro_candidato")

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
                        content=ft.Text("Candidatos.", size=20, weight="bold"),
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
                        content=ft.Text("Relatório.", size=20, weight="bold"),
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
                        content=ft.Text("Gráfico.", size=20, weight="bold"),
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
                        content=ft.Text("Administrador.", size=20, weight="bold"),
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
        [ft.TextButton("→ Voltar.", on_click=voltar)],
        alignment="end"
    )

    return ft.View(
        route="/admin_painel",
        bgcolor="#FCF8EC",
        controls=[
            ft.Stack(
                controls=[
                    # Moldura preta
                    ft.Container(
                        width=1700,
                        height=840,
                        bgcolor="black",
                        margin=ft.Margin(70, 70, 0, 0),
                    ),
                    # Moldura branca com conteúdo
                    ft.Container(
                        width=1700,
                        height=850,
                        bgcolor="white",
                        border=ft.border.all(width=1, color="black"),
                        content=ft.Column(
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
                            alignment="spaceBetween",  # ícones no centro, botão no final
                            expand=True
                        ),
                        padding=50,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
