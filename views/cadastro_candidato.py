import flet as ft

def cadastro_candidato_view():
    return ft.View(
        route="/cadastro_candidato",
        bgcolor="#FCF8EC",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
                content=ft.Column(
                    controls=[
                        # Área branca com borda e fundo
                        ft.Container(
                            bgcolor="white",
                            border=ft.border.all(width=1, color="black"),
                            padding=30,
                            expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.ResponsiveRow(
                                        columns=12,
                                        controls=[
                                            # Coluna esquerda
                                            ft.Container(
                                                col={"xs": 12, "md": 6},
                                                padding=10,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Container(
                                                            content=ft.Text("Presidente", size=60, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(0, 0, 0, 20)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Nome:", size=23, weight="bold"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(0, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.TextField(label="Informe o nome", color="black", width=500),
                                                            margin=ft.margin.only(bottom=20)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Número", size=23, weight="bold"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(0, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.TextField(label="Informe o número", color="black", width=500),
                                                            margin=ft.margin.only(bottom=20)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Partido:", size=23, weight="bold"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(0, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.TextField(label="Informe o Partido", color="black", width=500),
                                                            margin=ft.margin.only(bottom=20)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Sigla:", size=23, weight="bold"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(0, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=ft.TextField(label="Qual a sigla do partido?", color="black", width=500),
                                                            margin=ft.margin.only(bottom=20)
                                                        ),
                                                    ],
                                                    spacing=10,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                )
                                            ),


                                            # Coluna direita
                                            ft.Container(
                                                col={"xs": 12, "md": 6},
                                                padding=10,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Foto:", size=30, weight="bold", color="black"),
                                                        ft.Container(
                                                            content=ft.Text("Imagem aqui", size=20),
                                                            width=200,
                                                            height=300,
                                                            bgcolor="#f0f0f0",
                                                            alignment=ft.alignment.center
                                                        ),
                                                        ft.TextField(label="Descrição", color="black", height=200),
                                                        ft.Container(
                                                            content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                            alignment=ft.alignment.center,
                                                            width=150,
                                                            height=50,
                                                            bgcolor="#FCF8EC",
                                                            border=ft.border.all(1, "black"),
                                                            margin=ft.margin.only(top=5, left=5),
                                                            ink=True,
                                                            # on_click=login,
                                                            shadow=ft.BoxShadow(
                                                                spread_radius=0,
                                                                blur_radius=0,
                                                                color="black",
                                                                offset=ft.Offset(5, 5)
                                                            ),
                                                        ),
                                                    ],
                                                    spacing=20
                                                )
                                            ),
                                        ]
                                    ),
                                    # Botão voltar
                                    ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                "→ Voltar",
                                                on_click=lambda e: e.page.go("/admin_painel"),
                                                style=ft.ButtonStyle(
                                                    color="black",
                                                    overlay_color="transparent"
                                                )
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                spacing=30
                            )
                        )
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        ]
    )














# import flet as ft

# def cadastro_candidato_view():
#     return ft.View(
#         route="/cadastro_candidato",
#         bgcolor="#FCF8EC",
#         controls=[
#             ft.Stack(
#                 controls=[
#                     # Fundo preto
#                     ft.Container(
#                         width=1700,
#                         height=840,
#                         bgcolor="black",
#                         margin=ft.Margin(70, 70, 0, 0),
#                     ),
#                     # Área branca central
#                     ft.Container(
#                         width=1700,
#                         height=850,
#                         bgcolor="white",
#                         border=ft.border.all(width=1, color="black"),
#                         alignment=ft.alignment.center,
#                         content=ft.Column(
#                             controls=[
#                                 # Layout dividido em duas colunas lado a lado
#                                 ft.Row(
#                                     controls=[
#                                         # 🟩 Coluna esquerda - Dados do candidato
#                                         ft.Container(
#                                             width=800,
#                                             padding=20,
#                                             content=ft.Column(
#                                                 controls=[
#                                                     ft.Text("Presidente", size=40, weight="bold", color="black"),
#                                                     ft.TextField(label="Nome", width=400, color="black"),
#                                                     ft.TextField(label="Número", width=400, color="black"),
#                                                     ft.TextField(label="Partido", width=400, color="black"),
#                                                     ft.TextField(label="Sigla", width=400, color="black"),
#                                                 ],
#                                                 spacing=15,
#                                                 alignment=ft.MainAxisAlignment.START,
#                                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
#                                             )
#                                         ),
#                                         # 🟦 Coluna direita - Imagem, descrição, botão
#                                         ft.Container(
#                                             width=800,
#                                             padding=20,
#                                             content=ft.Column(
#                                                 controls=[
#                                                     ft.Container(
#                                                         content=ft.Text("Imagem aqui", size=20),
#                                                         width=200,
#                                                         height=200,
#                                                         bgcolor="#f0f0f0",
#                                                         alignment=ft.alignment.center
#                                                     ),
#                                                     ft.TextField(label="Descrição", width=400, color="black"),
#                                                     ft.ElevatedButton("Salvar", width=120, height=50),
#                                                 ],
#                                                 spacing=20,
#                                                 alignment=ft.MainAxisAlignment.START,
#                                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
#                                             )
#                                         ),
#                                     ],
#                                     alignment=ft.MainAxisAlignment.CENTER
#                                 ),
#                                 # 🔙 Botão "Voltar" na parte inferior direita
#                                 ft.Row(
#                                     controls=[
#                                         ft.TextButton(
#                                             "→ Voltar",
#                                             on_click=lambda e: e.page.go("/admin_painel"),
#                                             style=ft.ButtonStyle(
#                                                 color="black",
#                                                 overlay_color="transparent"
#                                             )
#                                         )
#                                     ],
#                                     alignment=ft.MainAxisAlignment.END
#                                 )
#                             ],
#                             expand=True,
#                             alignment=ft.MainAxisAlignment.START,
#                             horizontal_alignment=ft.CrossAxisAlignment.CENTER
#                         )
#                     ),
#                 ],
#                 expand=True,
#                 alignment=ft.alignment.center,
#             )
#         ],
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         vertical_alignment=ft.MainAxisAlignment.CENTER,
#     )
