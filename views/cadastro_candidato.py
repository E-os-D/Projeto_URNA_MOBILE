import flet as ft

def cadastro_candidato_view():
    def styled_textfield(label_text):
        return ft.TextField(
            label=label_text,
            bgcolor="#DFEDFF",
            color="black",
            width=600,
            border_radius=ft.border_radius.all(50),
            label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
            content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
        )

    return ft.View(
        route="/cadastro_candidato",
        bgcolor="#DFEDFF",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
                content=ft.Column(
                    controls=[
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
                                                            content=ft.Text("Presidente", size=70, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 40)
                                                        ),

                                                        # Nome
                                                        ft.Container(
                                                            content=ft.Text("Nome:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Informe o nome"),
                                                            margin=ft.margin.only(bottom=30)
                                                        ),

                                                        # Número
                                                        ft.Container(
                                                            content=ft.Text("Número:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Informe o número"),
                                                            margin=ft.margin.only(bottom=30)
                                                        ),

                                                        # Partido
                                                        ft.Container(
                                                            content=ft.Text("Partido:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Informe o Partido"),
                                                            margin=ft.margin.only(bottom=30)
                                                        ),

                                                        # Sigla
                                                        ft.Container(
                                                            content=ft.Text("Sigla:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Qual a sigla do partido?"),
                                                            margin=ft.margin.only(bottom=30)
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
                                                alignment=ft.alignment.center,
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Container(
                                                            content=ft.Text("Foto:", size=30, weight="bold", color="black"),
                                                            margin=ft.Margin(0, 50, 0, 0)
                                                        ),

                                                        ft.Container(
                                                            content=ft.Text("Imagem aqui", size=20),
                                                            width=200,
                                                            height=250,
                                                            bgcolor="#f0f0f0",
                                                            alignment=ft.alignment.center,
                                                            margin=ft.Margin(250, 0, 0, 0)
                                                        
                                                        ),
                                                    #AQUI È A DESCRIÇAÔ
                                                        ft.Container(
                                                            content=ft.Text("Descrição:", size=30, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            
                                                        ),
                                                        ft.TextField(
                                                            label="",
                                                            color="black",
                                                            height=200,
                                                            width=600,
                                                            bgcolor="#DFEDFF",
                                                            label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                                                            content_padding=ft.Padding(top=22, bottom=50, left=16, right=16),
                                                            multiline=True,
                                                            max_lines=5
                                                        ),

                                                        ft.Container(
                                                            content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                            alignment=ft.alignment.center,
                                                            width=150,
                                                            height=50,
                                                            bgcolor="#DFEDFF",
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
