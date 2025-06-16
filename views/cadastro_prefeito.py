import flet as ft
import sqlite3
import os
import base64

def cadastro_prefeito_view():
    nome = ft.Ref[ft.TextField]()
    numero = ft.Ref[ft.TextField]() # Referência para o número do prefeito
    partido_dropdown = ft.Ref[ft.Dropdown]()
    descricao = ft.Ref[ft.TextField]()
    mensagem = ft.Text(value="", color="red")

    placeholder_image_path = "img/placeholder_foto.png"
    
    foto_bytes = {"value": None} 

    if os.path.exists(placeholder_image_path):
        try:
            with open(placeholder_image_path, "rb") as f:
                placeholder_image_content_bytes = f.read()
            initial_image_content = ft.Image(
                src_base64=base64.b64encode(placeholder_image_content_bytes).decode('utf-8'),
                width=180,
                height=180,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Erro ao carregar imagem ou não encontrada")
            )
            foto_bytes["value"] = placeholder_image_content_bytes
        except Exception as e:
            print(f"Erro ao carregar a imagem placeholder: {e}")
            initial_image_content = ft.Text("Nenhuma imagem selecionada", text_align=ft.TextAlign.CENTER)
            foto_bytes["value"] = None
    else:
        print(f"Aviso: Imagem placeholder não encontrada em {placeholder_image_path}")
        initial_image_content = ft.Text("Nenhuma imagem selecionada", text_align=ft.TextAlign.CENTER)
        foto_bytes["value"] = None

    imagem_preview_container = ft.Container(
        content=initial_image_content,
        width=180,
        height=180,
        border=ft.border.all(1, "black"),
        alignment=ft.alignment.center,
        bgcolor="#DFEDFF",
        border_radius=ft.border_radius.all(10),
    )

    def styled_textfield(ref, hint_text="", label_text=""):
        return ft.Column(
            controls=[
                ft.Text(label_text, size=23, weight="bold", color="black"),
                ft.TextField(
                    ref=ref,
                    bgcolor="#DFEDFF",
                    color="black",
                    width=450,
                    height=55,
                    border_radius=ft.border_radius.all(10),
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                    content_padding=ft.Padding(top=15, bottom=15, left=16, right=16),
                    hint_text=hint_text,
                    border_color="black",
                    border_width=1,
                    text_align=ft.TextAlign.LEFT,
                ),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

    def styled_dropdown(ref, options, hint, label_text=""):
        return ft.Column(
            controls=[
                ft.Text(label_text, size=23, weight="bold", color="black"),
                ft.Dropdown(
                    ref=ref,
                    options=options,
                    width=450,
                    border_radius=ft.border_radius.all(10),
                    color="black",
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                    content_padding=ft.Padding(top=10, bottom=10, left=16, right=16),
                    hint_text=hint,
                    border_color="black",
                    border_width=1,
                ),
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

    def carregar_partidos():
        conn = None
        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id_partido, nome FROM Partidos ORDER BY nome")
            partidos = cursor.fetchall()
            return [ft.dropdown.Option(str(id_), label) for id_, label in partidos]
        except sqlite3.Error as ex:
            mensagem.value = f"Erro ao carregar partidos: {str(ex)}"
            return []
        finally:
            if conn:
                conn.close()

    def selecionar_imagem(e: ft.FilePickerResultEvent):
        if e.files:
            caminho = e.files[0].path
            try:
                with open(caminho, "rb") as f:
                    file_content = f.read()
                foto_bytes["value"] = file_content
                imagem_preview_container.content = ft.Image(
                    src_base64=base64.b64encode(file_content).decode('utf-8'),
                    width=180,
                    height=180,
                    fit=ft.ImageFit.CONTAIN
                )
                mensagem.value = ""
            except Exception as ex:
                mensagem.value = f"Erro ao carregar a imagem: {str(ex)}"
                foto_bytes["value"] = None
                imagem_preview_container.content = initial_image_content
        else:
            mensagem.value = "Seleção de imagem cancelada."
            foto_bytes["value"] = None
            imagem_preview_container.content = initial_image_content
        imagem_preview_container.update()
        e.page.update()

    def cadastrar_prefeito(e):
        nome_val = nome.current.value.strip()
        numero_val = numero.current.value.strip()
        descricao_val = descricao.current.value.strip()
        partido_sel = partido_dropdown.current.value
        foto_data = foto_bytes["value"]

        if not all([nome_val, numero_val, partido_sel]):
            mensagem.value = "Preencha todos os campos obrigatórios!"
            e.page.update()
            return

        if foto_data is None:
            mensagem.value = "Por favor, selecione uma imagem para o candidato!"
            e.page.update()
            return

        conn = None
        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()
            id_partido = int(partido_sel)

            # Verifica se o número do prefeito já existe
            cursor.execute("SELECT * FROM Prefeito WHERE id_número_prefeito = ?", (numero_val,))
            if cursor.fetchone():
                mensagem.value = "Número já cadastrado para um prefeito!"
            else:
                cursor.execute("""
                    INSERT INTO Prefeito (id_número_prefeito, nome, foto, id_partido, descrição)
                    VALUES (?, ?, ?, ?, ?)
                """, (numero_val, nome_val, foto_data, id_partido, descricao_val))
                conn.commit()
                mensagem.value = "Candidato a prefeito cadastrado com sucesso!"

                nome.current.value = ""
                numero.current.value = ""
                partido_dropdown.current.value = None
                descricao.current.value = ""
                foto_bytes["value"] = None
                imagem_preview_container.content = initial_image_content
                imagem_preview_container.update()
                nome.current.focus()
                e.page.update()
        except sqlite3.IntegrityError as ex:
            if "UNIQUE constraint failed: Prefeito.id_número_prefeito" in str(ex):
                mensagem.value = "Erro: O número do prefeito já está em uso!"
            else:
                mensagem.value = f"Erro de integridade ao cadastrar: {str(ex)}"
        except ValueError:
            mensagem.value = "Número do partido inválido."
        except Exception as ex:
            mensagem.value = f"Erro inesperado ao cadastrar: {str(ex)}"
        finally:
            if conn:
                conn.close()
            e.page.update()

    dropdown_items = carregar_partidos()
    file_picker = ft.FilePicker(on_result=selecionar_imagem)

    return ft.View(
        route="/cadastro_prefeito",
        bgcolor="#B0C4DE",
        padding=20,
        controls=[
            file_picker,
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=30,
                        bgcolor="white",
                        border_radius=ft.border_radius.all(10),
                        border=ft.border.all(1, "black"),
                        shadow=ft.BoxShadow(color="black", offset=ft.Offset(8, 8)),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.ResponsiveRow(
                                    columns=12,
                                    spacing=50,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        ft.Container(
                                            col={"xs": 12, "md": 6},
                                            content=ft.Column(
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Text("Prefeito", size=50, weight="bold", color="black"),
                                                        alignment=ft.alignment.center_left,
                                                        margin=ft.Margin(left=0, top=0, right=0, bottom=40),
                                                    ),
                                                    styled_textfield(nome, "Ex: João da Silva", "Nome:"),
                                                    styled_textfield(numero, "Ex: 13", "Número:"),
                                                    styled_dropdown(partido_dropdown, dropdown_items, "Selecione o partido", "Partido:"),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                                spacing=30
                                            ),
                                            alignment=ft.alignment.top_left
                                        ),
                                        ft.Container(
                                            col={"xs": 12, "md": 6},
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Foto:", size=23, weight="bold", color="black"),
                                                            ft.Container(width=10),
                                                            imagem_preview_container,
                                                        ],
                                                        vertical_alignment=ft.CrossAxisAlignment.START
                                                    ),
                                                    ft.Container(height=10),
                                                    ft.Container(
                                                        content=ft.Text("Selecionar imagem", size=14, color="black"),
                                                        alignment=ft.alignment.center,
                                                        width=170,
                                                        height=40,
                                                        bgcolor="#DFEDFF",
                                                        border=ft.border.all(1, "black"),
                                                        ink=True,
                                                        on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png", "gif"]),
                                                        shadow=ft.BoxShadow(
                                                            spread_radius=0, blur_radius=0, color="black", offset=ft.Offset(5, 5)
                                                        )
                                                    ),
                                                    ft.Container(height=20),
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text("Descrição:", size=23, weight="bold", color="black"),
                                                            ft.TextField(
                                                                ref=descricao,
                                                                color="black",
                                                                height=140,
                                                                width=450,
                                                                bgcolor="#DFEDFF",
                                                                multiline=True,
                                                                min_lines=4,
                                                                max_lines=8,
                                                                content_padding=ft.Padding(top=15, bottom=15, left=16, right=16),
                                                                border_radius=ft.border_radius.all(10),
                                                                label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                                                                border_color="black",
                                                                border_width=1,
                                                            ),
                                                        ],
                                                        horizontal_alignment=ft.CrossAxisAlignment.START
                                                    ),
                                                    ft.Container(height=20),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Container(
                                                                content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                                alignment=ft.alignment.center,
                                                                width=180,
                                                                height=50,
                                                                bgcolor="#DFEDFF",
                                                                border=ft.border.all(1, "black"),
                                                                ink=True,
                                                                on_click=cadastrar_prefeito,
                                                                shadow=ft.BoxShadow(
                                                                    spread_radius=0, blur_radius=0, color="black", offset=ft.Offset(8, 8)
                                                                ),
                                                            ),
                                                        ],
                                                        alignment=ft.MainAxisAlignment.START,
                                                        expand=True
                                                    ),
                                                    ft.Container(height=10),
                                                    mensagem,
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                                spacing=0
                                            ),
                                            alignment=ft.alignment.top_left
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            "← Voltar",
                                            on_click=lambda e: e.page.go("/admin_painel_cadastro"),
                                            style=ft.ButtonStyle(
                                                color="black",
                                                overlay_color="transparent",
                                                text_style=ft.TextStyle(size=14)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    expand=True
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.START,
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE
                        )
                    )
                ]
            )
        ]
    )