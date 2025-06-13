import flet as ft
import sqlite3

def cadastro_candidato_view():
    # Refs para os campos
    nome = ft.Ref[ft.TextField]()
    numero = ft.Ref[ft.TextField]()
    partido_dropdown = ft.Ref[ft.Dropdown]()
    descricao = ft.Ref[ft.TextField]()
    mensagem = ft.Text(value="", color="red")

    # Campo de texto estilizado
    def styled_textfield(label_text, ref):
        return ft.TextField(
            label=label_text,
            ref=ref,
            bgcolor="#DFEDFF",
            color="black",
            width=600,
            border_radius=ft.border_radius.all(50),
            label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
            content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
        )

    # Dropdown estilizado (igual aos inputs)
    def styled_dropdown(ref, options, hint):
        return ft.Dropdown(
            ref=ref,
            options=options,
            width=600,
            border_radius=ft.border_radius.all(10),
            color="#DFEDFF",
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
            content_padding=ft.Padding(top=20, bottom=20, left=16, right=16),
            hint_text=hint
        )

    # Carregar os partidos do banco
    def carregar_partidos():
        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id_partido, nome FROM Partidos ORDER BY nome")
            partidos = cursor.fetchall()
            return [ft.dropdown.Option(str(id_), label) for id_, label in partidos]
        except Exception as ex:
            mensagem.value = f"Erro ao carregar partidos: {str(ex)}"
            return []
        finally:
            conn.close()

    # Função de cadastro
    def cadastrar_candidato(e):
        nome_val = nome.current.value.strip()
        numero_val = numero.current.value.strip()
        descricao_val = descricao.current.value.strip()
        partido_sel = partido_dropdown.current.value

        if not all([nome_val, numero_val, partido_sel]):
            mensagem.value = "Preencha todos os campos obrigatórios!"
            e.page.update()
            return

        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()
            id_partido = int(partido_sel)

            cursor.execute("SELECT * FROM Presidente WHERE id_número_presidente = ?", (numero_val,))
            if cursor.fetchone():
                mensagem.value = "Número já cadastrado!"
            else:
                cursor.execute("""
                    INSERT INTO Presidente (id_número_presidente, nome, foto, id_partido, descrição)
                    VALUES (?, ?, ?, ?, ?)
                """, (numero_val, nome_val, None, id_partido, descricao_val))
                conn.commit()
                mensagem.value = "Candidato cadastrado com sucesso!"

                nome.current.value = ""
                numero.current.value = ""
                partido_dropdown.current.value = None
                descricao.current.value = ""

        except Exception as ex:
            mensagem.value = f"Erro ao cadastrar: {str(ex)}"
        finally:
            conn.close()
            e.page.update()

    # Carregar partidos
    dropdown_items = carregar_partidos()

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
                                                        ft.Container(
                                                            content=ft.Text("Nome:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Informe o nome", nome),
                                                            margin=ft.margin.only(bottom=30)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Número:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_textfield("Informe o número", numero),
                                                            margin=ft.margin.only(bottom=30)
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text("Partido:", size=23, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left,
                                                            margin=ft.Margin(80, 0, 0, 0)
                                                        ),
                                                        ft.Container(
                                                            content=styled_dropdown(partido_dropdown, dropdown_items, "Selecione o partido"),
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
                                                        ft.Container(
                                                            content=ft.Text("Descrição:", size=30, weight="bold", color="black"),
                                                            alignment=ft.alignment.top_left
                                                        ),
                                                        ft.TextField(
                                                            ref=descricao,
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
                                                        mensagem,
                                                        ft.Container(
                                                            content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                            alignment=ft.alignment.center,
                                                            width=150,
                                                            height=50,
                                                            bgcolor="#DFEDFF",
                                                            border=ft.border.all(1, "black"),
                                                            margin=ft.margin.only(top=5, left=5),
                                                            ink=True,
                                                            on_click=cadastrar_candidato,
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
