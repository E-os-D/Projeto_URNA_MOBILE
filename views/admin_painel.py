# import flet as ft

# def admin_painel_view():
#     def voltar(e):
#         e.page.go("/")  # ou rota anterior

#     def ir_candidatos(e):
#         e.page.go("/cadastro_candidato")

#     def ir_relatorio(e):
#         e.page.go("/resultado")

#     def ir_grafico(e):
#         e.page.go("/graficos")

#     def ir_admin(e):
#         e.page.go("/cadastro_admin")

#     # Botões de navegação (ícones com texto)
#     opcoes = ft.Row(
#         controls=[
#             ft.GestureDetector(
#                 content=ft.Column([
#                     ft.Image(src="img/admin_candidatos.png", width=150),
#                     ft.Container(
#                         content=ft.Text("Candidatos.", weight=ft.FontWeight.BOLD, size=20),
#                         alignment=ft.alignment.center_right,
#                         width=150
#                     )
#                 ], horizontal_alignment="center"),
#                 on_tap=ir_candidatos
#             ),
#             ft.GestureDetector(
#                 content=ft.Column([
#                     ft.Image(src="img/admin_relatorio.png", width=150),
#                     ft.Container(
#                         content=ft.Text("Relatório.", weight=ft.FontWeight.BOLD, size=20),
#                         alignment=ft.alignment.center_right,
#                         width=150
#                     )
#                 ], horizontal_alignment="center"),
#                 on_tap=ir_relatorio
#             )
#         ],
#         alignment="center",
#         spacing=80
#     )

#     opcoes2 = ft.Row(
#         controls=[
#             ft.GestureDetector(
#                 content=ft.Column([
#                     ft.Image(src="img/admin_grafico.png", width=150),
#                     ft.Container(
#                         content=ft.Text("Gráfico.", weight=ft.FontWeight.BOLD, size=20),
#                         alignment=ft.alignment.center_right,
#                         width=150
#                     )
#                 ], horizontal_alignment="center"),
#                 on_tap=ir_grafico
#             ),
#             ft.GestureDetector(
#                 content=ft.Column([
#                     ft.Image(src="img/admin_administrador.png", width=150),
#                     ft.Container(
#                         content=ft.Text("Administrador.", weight=ft.FontWeight.BOLD, size=20),
#                         alignment=ft.alignment.center_right,
#                         width=150
#                     )
#                 ], horizontal_alignment="center"),
#                 on_tap=ir_admin
#             )
#         ],
#         alignment="center",
#         spacing=80
#     )

#     # Botão fixo no canto inferior direito DENTRO da moldura branca
#     botao_voltar = ft.Container(
#         content=ft.TextButton("→ Voltar.", on_click=voltar),
#         alignment=ft.alignment.bottom_right,
#         padding=ft.Padding(0, 0, 10, 10)
#     )

#     # Moldura branca com conteúdo e botão no canto
#     painel_conteudo = ft.Container(
#         width=1700,
#         height=850,
#         bgcolor="white",
#         border=ft.border.all(width=1, color="black"),
#         content=ft.Stack(
#             controls=[
#                 ft.Column(
#                     [opcoes, opcoes2],
#                     alignment="center",
#                     spacing=50,
#                     expand=True
#                 ),
#                 botao_voltar
#             ],
#             expand=True
#         ),
#         padding=50
#     )

#     return ft.View(
#         route="/admin_painel",
#         bgcolor="#FCF8EC",
#         controls=[
#             ft.Stack(
#                 controls=[
#                     ft.Container(
#                         width=1700,
#                         height=840,
#                         bgcolor="black",
#                         margin=ft.Margin(70, 70, 0, 0),
#                     ),
#                     painel_conteudo
#                 ],
#                 expand=True,
#                 alignment=ft.alignment.center
#             )
#         ],
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         vertical_alignment=ft.MainAxisAlignment.CENTER
#     )



import flet as ft

def admin_painel_view():
    def voltar(e):
        e.page.go("/")  # ou rota anterior

    def ir_candidatos(e):
        e.page.go("/cadastro_candidato")

    def ir_relatorio(e):
        e.page.go("/resultado")

    def ir_grafico(e):
        e.page.go("/graficos")

    def ir_admin(e):
        e.page.go("/cadastro_admin")

    # Cria os botões como imagens com textos, dentro de GestureDetector
    opcoes = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_candidatos.png", width=150),
                    ft.Container(
                        content=ft.Text("Candidatos."),
                        alignment=ft.alignment.center_right,
                        width=150  # mesma largura da imagem
                    )

                ], horizontal_alignment="center"),
                on_tap=ir_candidatos
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_relatorio.png", width=150),
                    ft.Container(
                        content=ft.Text("Relatório."),
                        alignment=ft.alignment.center_right,
                        width=150  # mesma largura da imagem
                    )

                ], horizontal_alignment="center"),
                on_tap=ir_relatorio
            )
        ],
        alignment="center",
        spacing=80
    )

    opcoes2 = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_grafico.png", width=150),
                    ft.Container(
                        content=ft.Text("Gráfico."),
                        alignment=ft.alignment.center_right,
                        width=150  # mesma largura da imagem
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_grafico
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_administrador.png", width=150),
                    ft.Container(
                        content=ft.Text("Administrador."),
                        alignment=ft.alignment.center_right,
                        width=150  # mesma largura da imagem
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_admin
            )
        ],
        alignment="center",
        spacing=80
    )

    voltar_row = ft.Row(
        [ft.TextButton("→ Voltar.", on_click=voltar)],
        alignment="end"
    )

    return ft.View(
        route="/admin_painel",
        bgcolor="#FCF8EC",  # fundo igual ao da home
        controls=[
            ft.Stack(
                controls=[
                    # Moldura preta (fundo)
                    ft.Container(
                        width=1700,
                        height=840,
                        bgcolor="black",
                        margin=ft.Margin(70, 70, 0, 0),  # deslocado p/ parecer sombra
                    ),

                    # Moldura branca (painel principal com conteúdo)
                    ft.Container(
                        width=1700,
                        height=850,
                        bgcolor="white",
                        border=ft.border.all(width=1, color="black"),
                        content=ft.Column(
                            [opcoes, opcoes2, voltar_row],
                            alignment="center",
                            spacing=50
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