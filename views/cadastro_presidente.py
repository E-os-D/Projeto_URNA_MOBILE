import flet as ft
import sqlite3
import os
import base64

def cadastro_presidente_view():
    nome = ft.Ref[ft.TextField]()
    numero = ft.Ref[ft.TextField]()
    partido_dropdown = ft.Ref[ft.Dropdown]()
    descricao = ft.Ref[ft.TextField]()
    mensagem = ft.Text(value="", color="red")

    # Caminho da imagem placeholder local (verifique se "placeholder_foto.png" existe na pasta 'img')
    # Use a relative path that works from the script's execution directory
    placeholder_image_path = "img/placeholder_foto.png"
    
    # Variável global para armazenar os bytes da imagem selecionada
    foto_bytes = {"value": None} 

    # Carrega os bytes da imagem placeholder se ela existir, caso contrário, usa um texto de fallback
    if os.path.exists(placeholder_image_path):
        try:
            with open(placeholder_image_path, "rb") as f:
                placeholder_image_content_bytes = f.read()
            # Codifica para base64 para o ft.Image src_base64
            initial_image_content = ft.Image(
                src_base64=base64.b64encode(placeholder_image_content_bytes).decode('utf-8'),
                width=180, # Ajustado para corresponder à largura do contêiner
                height=180, # Ajustado para corresponder à altura do contêiner
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Erro ao carregar imagem ou não encontrada")
            )
            foto_bytes["value"] = placeholder_image_content_bytes # Inicializa com os bytes do placeholder
        except Exception as e:
            print(f"Erro ao carregar a imagem placeholder: {e}")
            initial_image_content = ft.Text("Nenhuma imagem selecionada", text_align=ft.TextAlign.CENTER)
            foto_bytes["value"] = None # Reseta para None se houver erro ao carregar o placeholder
    else:
        print(f"Aviso: Imagem placeholder não encontrada em {placeholder_image_path}")
        initial_image_content = ft.Text("Nenhuma imagem selecionada", text_align=ft.TextAlign.CENTER)
        foto_bytes["value"] = None # Nenhum byte de placeholder se o arquivo não existir

    # Contêiner principal para a pré-visualização da imagem, inicialmente mostrando o placeholder
    imagem_preview_container = ft.Container(
        content=initial_image_content, # Inicia com a imagem placeholder ou texto
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
                    width=450, # Increased width for text fields
                    height=55, # Adjusted height for better visual
                    border_radius=ft.border_radius.all(10),
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                    content_padding=ft.Padding(top=15, bottom=15, left=16, right=16),
                    hint_text=hint_text,
                    border_color="black",
                    border_width=1,
                    text_align=ft.TextAlign.LEFT,
                ),
            ],
            spacing=5, # Espaçamento entre o label e o campo
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

    def styled_dropdown(ref, options, hint, label_text=""):
        return ft.Column(
            controls=[
                ft.Text(label_text, size=23, weight="bold", color="black"),
                ft.Dropdown(
                    ref=ref,
                    options=options,
                    width=450, # Increased width for dropdown
                    border_radius=ft.border_radius.all(10),
                    color="black",
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                    content_padding=ft.Padding(top=10, bottom=10, left=16, right=16),
                    hint_text=hint,
                    border_color="black",
                    border_width=1,
                ),
            ],
            spacing=5, # Espaçamento entre o label e o campo
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

    def carregar_partidos():
        """Carrega os partidos do banco de dados."""
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
        """Callback para o FilePicker, lê o arquivo de imagem e atualiza a pré-visualização."""
        if e.files:
            caminho = e.files[0].path
            try:
                with open(caminho, "rb") as f:
                    file_content = f.read()
                foto_bytes["value"] = file_content # Armazena os bytes da imagem
                # Converte os bytes para base64 para exibir no Flet
                imagem_preview_container.content = ft.Image(
                    src_base64=base64.b64encode(file_content).decode('utf-8'),
                    width=180,
                    height=180,
                    fit=ft.ImageFit.CONTAIN
                )
                mensagem.value = "" # Limpa mensagens anteriores
            except Exception as ex:
                mensagem.value = f"Erro ao carregar a imagem: {str(ex)}"
                foto_bytes["value"] = None # Reseta a variável de bytes da imagem
                imagem_preview_container.content = initial_image_content # Volta para o placeholder ou texto
        else:
            mensagem.value = "Seleção de imagem cancelada."
            foto_bytes["value"] = None # Reseta a variável de bytes da imagem se a seleção for cancelada
            imagem_preview_container.content = initial_image_content # Volta para o placeholder ou texto
        imagem_preview_container.update()
        e.page.update()

    def cadastrar_presidente(e):
        """Função para cadastrar o presidente no banco de dados."""
        nome_val = nome.current.value.strip()
        numero_val = numero.current.value.strip()
        descricao_val = descricao.current.value.strip()
        partido_sel = partido_dropdown.current.value
        foto_data = foto_bytes["value"] # Obtém os bytes da imagem

        if not all([nome_val, numero_val, partido_sel]):
            mensagem.value = "Preencha todos os campos obrigatórios!"
            e.page.update()
            return

        if foto_data is None: # Verifica se os bytes da imagem estão disponíveis
            mensagem.value = "Por favor, selecione uma imagem para o candidato!"
            e.page.update()
            return

        conn = None
        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()
            id_partido = int(partido_sel)

            # Verifica se o número do presidente já existe
            cursor.execute("SELECT * FROM Presidente WHERE id_número_presidente = ?", (numero_val,))
            if cursor.fetchone():
                mensagem.value = "Número já cadastrado para um presidente!"
            else:
                # Insere os dados do presidente, incluindo os bytes da foto (BLOB)
                cursor.execute("""
                    INSERT INTO Presidente (id_número_presidente, nome, foto, id_partido, descrição)
                    VALUES (?, ?, ?, ?, ?)
                """, (numero_val, nome_val, foto_data, id_partido, descricao_val))
                conn.commit()
                mensagem.value = "Candidato cadastrado com sucesso!"

                # Limpar campos após o cadastro bem-sucedido
                nome.current.value = ""
                numero.current.value = ""
                partido_dropdown.current.value = None # Reseta o dropdown
                descricao.current.value = ""
                foto_bytes["value"] = None # Limpa os bytes da imagem armazenados
                imagem_preview_container.content = initial_image_content # Volta para o placeholder
                imagem_preview_container.update() # Atualiza a UI do container
                nome.current.focus() # Coloca o foco no primeiro campo
        except sqlite3.IntegrityError as ex:
            if "UNIQUE constraint failed: Presidente.id_número_presidente" in str(ex):
                mensagem.value = "Erro: O número do presidente já está em uso!"
            else:
                mensagem.value = f"Erro de integridade ao cadastrar: {str(ex)}"
        except ValueError:
            mensagem.value = "Número do partido inválido."
        except Exception as ex:
            mensagem.value = f"Erro inesperado ao cadastrar: {str(ex)}"
        finally:
            if conn:
                conn.close()
            e.page.update() # Atualiza a página para mostrar a mensagem

    dropdown_items = carregar_partidos()
    file_picker = ft.FilePicker(on_result=selecionar_imagem)

    return ft.View(
        route="/cadastro_presidente", # Updated route
        bgcolor="#B0C4DE",
        padding=20,
        controls=[
            file_picker, # Adicione o file_picker ao controle da View
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        padding=30,
                        bgcolor="white",
                        border_radius=ft.border_radius.all(10), # Added border radius to main container
                        border=ft.border.all(1, "black"),
                        shadow=ft.BoxShadow(color="black", offset=ft.Offset(8, 8)),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.ResponsiveRow(
                                    columns=12,
                                    spacing=50, # Increased spacing between columns
                                    vertical_alignment=ft.CrossAxisAlignment.START, # Align content to the top
                                    controls=[
                                        # Coluna Esquerda: Nome, Número, Partido
                                        ft.Container(
                                            col={"xs": 12, "md": 6},
                                            content=ft.Column(
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Text("Presidente", size=50, weight="bold", color="black"),
                                                        alignment=ft.alignment.center_left,
                                                        margin=ft.Margin(left=0, top=0, right=0, bottom=40),
                                                    ),
                                                    styled_textfield(nome, "Ex: João da Silva", "Nome:"),
                                                    styled_textfield(numero, "Ex: 13", "Número:"),
                                                    styled_dropdown(partido_dropdown, dropdown_items, "Selecione o partido", "Partido:"),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                                spacing=30 # Adjusted spacing between input groups
                                            ),
                                            alignment=ft.alignment.top_left
                                        ),
                                        # Coluna Direita: Foto, Descrição, Botões
                                        ft.Container(
                                            col={"xs": 12, "md": 6},
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row( # Novo Row para "Foto:" e imagem
                                                        controls=[
                                                            ft.Text("Foto:", size=23, weight="bold", color="black"),
                                                            ft.Container(width=10), # Espaço entre o texto e a imagem
                                                            imagem_preview_container,
                                                        ],
                                                        vertical_alignment=ft.CrossAxisAlignment.START # Alinha verticalmente no centro
                                                    ),
                                                    ft.Container(height=10), # Espaçamento
                                                    ft.Container(
                                                        content=ft.Text("Selecionar imagem", size=14, color="black"),
                                                        alignment=ft.alignment.center,
                                                        width=170, # Adjusted width to match image preview container
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
                                                    ft.Column( # Envolve a descrição para controle de alinhamento
                                                        controls=[
                                                            ft.Text("Descrição:", size=23, weight="bold", color="black"),
                                                            ft.TextField(
                                                                ref=descricao,
                                                                color="black",
                                                                height=140, # Increased height for description
                                                                width=450, # Increased width to match other fields
                                                                bgcolor="#DFEDFF",
                                                                multiline=True,
                                                                min_lines=4, # Adiciona esta linha para garantir 4 linhas visíveis
                                                                max_lines=8, # Increased max_lines to match new height
                                                                content_padding=ft.Padding(top=15, bottom=15, left=16, right=16),
                                                                border_radius=ft.border_radius.all(10),
                                                                label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                                                                border_color="black",
                                                                border_width=1,
                                                            ),
                                                        ],
                                                        horizontal_alignment=ft.CrossAxisAlignment.START # Alinha a descrição à esquerda
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
                                                                on_click=cadastrar_presidente,
                                                                shadow=ft.BoxShadow(
                                                                    spread_radius=0, blur_radius=0, color="black", offset=ft.Offset(8, 8)
                                                                ),
                                                            ),
                                                        ],
                                                        alignment=ft.MainAxisAlignment.START, # Aligns the button to the start (left)
                                                        expand=True # Allows the row to take available width
                                                    ),
                                                    ft.Container(height=10),
                                                    mensagem,
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START, # Alinha todo o conteúdo da coluna direita à esquerda
                                                spacing=0 # Maintain original spacing for this column
                                            ),
                                            alignment=ft.alignment.top_left # Alinha a coluna da direita ao topo e à esquerda
                                        ),
                                    ],
                                ),
                                # Moved the "Voltar" button outside the ResponsiveRow for better control
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
                                    alignment=ft.MainAxisAlignment.START, # Align to the start (left)
                                    expand=True # Allows the row to take available width
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