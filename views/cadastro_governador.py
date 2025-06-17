import flet as ft
import sqlite3
import os
import base64

def cadastro_governador_view(): # Alterado o nome da função
    nome = ft.Ref[ft.TextField]()
    numero = ft.Ref[ft.TextField]()
    partido_dropdown = ft.Ref[ft.Dropdown]()
    descricao = ft.Ref[ft.TextField]()
    mensagem = ft.Text(value="", color="red")

    # Caminho da imagem placeholder local (verifique se "placeholder_foto.png" existe na pasta 'img')
    placeholder_image_path = "img/placeholder_foto.png"
    
    # Variável global para armazenar os bytes da imagem selecionada
    foto_bytes = {"value": None} 

    # Carrega os bytes da imagem placeholder se ela existir, caso contrário, usa um texto de fallback
    initial_image_content = ft.Text("Nenhuma imagem selecionada", text_align=ft.TextAlign.CENTER, color="black") # Default fallback
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
                error_content=ft.Text("Erro ao carregar imagem ou não encontrada", color="black")
            )
            foto_bytes["value"] = placeholder_image_content_bytes # Inicializa com os bytes do placeholder
        except Exception as e:
            print(f"Erro ao carregar a imagem placeholder: {e}")
            foto_bytes["value"] = None # Reseta para None se houver erro ao carregar o placeholder
    else:
        print(f"Aviso: Imagem placeholder não encontrada em {placeholder_image_path}")
        foto_bytes["value"] = None # Nenhum byte de placeholder se o arquivo não existir

    # Contêiner principal para a pré-visualização da imagem, inicialmente mostrando o placeholder
    imagem_preview_container = ft.Container(
        content=initial_image_content, # Inicia com a imagem placeholder ou texto
        width=150, # Mantido fixo para a visualização da imagem
        height=180, # Mantido fixo para a visualização da imagem
        border=ft.border.all(1, "black"),
        alignment=ft.alignment.center,
        bgcolor="#DFEDFF",
    )

    def styled_textfield(ref, hint_text="", label_text=""):
        return ft.Column(
            controls=[
                ft.Text(label_text, size=22, weight="bold", color="black"), # Adjusted label size
                ft.TextField(
                    ref=ref,
                    bgcolor="#DFEDFF",
                    color="black",
                    border_radius=ft.border_radius.all(5),
                    label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500), 
                    content_padding=ft.Padding(top=15, bottom=15, left=16, right=16), 
                    hint_text=hint_text,
                    hint_style=ft.TextStyle(color=ft.Colors.BLACK54), 
                    border_color="black", 
                    border_width=1,
                    text_align=ft.TextAlign.LEFT,
                    expand=True, # Permite que o campo de texto se expanda horizontalmente
                ),
            ],
            spacing=5, 
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True, # Permite que a coluna se expanda
        )

    def styled_dropdown(ref, options, hint, label_text=""):
        return ft.Column(
            controls=[
                ft.Text(label_text, size=22, weight="bold", color="black"),
                ft.Dropdown(
                    ref=ref,
                    options=options,
                    border_radius=ft.border_radius.all(5),
                    color="black",
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                    content_padding=ft.Padding(top=10, bottom=10, left=16, right=16),
                    hint_text=hint,
                    hint_style=ft.TextStyle(color=ft.Colors.BLACK54), 
                    border_color="black", 
                    border_width=1,
                    expand=True, # Permite que o dropdown se expanda horizontalmente
                ),
            ],
            spacing=5, 
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True, # Permite que a coluna se expanda
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

    def cadastrar_governador(e): # Alterado o nome da função
        """Função para cadastrar o governador no banco de dados."""
        nome_val = nome.current.value.strip()
        numero_val = numero.current.value.strip()
        descricao_val = descricao.current.value.strip()
        partido_sel = partido_dropdown.current.value
        foto_data = foto_bytes["value"] 

        if not all([nome_val, numero_val, partido_sel]):
            mensagem.value = "Preencha todos os campos obrigatórios!"
            e.page.update()
            return

        try:
            numero_int = int(numero_val)
            if not (10 <= numero_int <= 99): # Governador também costuma ter 2 dígitos
                mensagem.value = "O número do governador deve ser um inteiro de 2 dígitos (ex: 13, 22)." # Alterado o texto
                e.page.update()
                return
        except ValueError:
            mensagem.value = "O número do governador deve ser um valor numérico válido." # Alterado o texto
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

            # Alterado o nome da tabela e da coluna para Governador
            cursor.execute("SELECT * FROM Governador WHERE id_número_governador = ?", (numero_val,))
            if cursor.fetchone():
                mensagem.value = "Número já cadastrado para um governador!" # Alterado o texto
            else:
                # Alterado o nome da tabela e das colunas para Governador
                cursor.execute("""
                    INSERT INTO Governador (id_número_governador, nome, foto, id_partido, descrição)
                    VALUES (?, ?, ?, ?, ?)
                """, (numero_val, nome_val, foto_data, id_partido, descricao_val))
                conn.commit()
                mensagem.value = "Candidato cadastrado com sucesso!"

                nome.current.value = ""
                numero.current.value = ""
                partido_dropdown.current.value = None 
                descricao.current.value = ""
                foto_bytes["value"] = None 
                imagem_preview_container.content = initial_image_content 
                imagem_preview_container.update() 
                nome.current.focus() 
        except sqlite3.IntegrityError as ex:
            # Alterado o nome da tabela para Governador
            if "UNIQUE constraint failed: Governador.id_número_governador" in str(ex):
                mensagem.value = "Erro: O número do governador já está em uso!" # Alterado o texto
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
        route="/cadastro_governador", # Alterado a rota
        bgcolor="#B0C4DE",
        controls=[
            file_picker, 
            ft.ResponsiveRow( # Usamos ResponsiveRow aqui para centralizar e controlar a largura
                [
                    ft.Container( # Este é o container que representa o "quadrado branco"
                        col={"xs": 12, "sm": 10, "md": 8, "lg": 7, "xl": 6}, # Ajuste estas colunas para o tamanho desejado
                        # Sem width/height fixos aqui para o container principal para permitir flexibilidade
                        # max_width pode ser usado se você quiser um limite no tamanho total do formulário
                        padding=30, 
                        bgcolor="white",
                        border=ft.border.all(1, "black"),
                        shadow=ft.BoxShadow(
                            color="black",
                            offset=ft.Offset(8, 8), 
                            blur_radius=0, 
                            spread_radius=0
                        ),
                        content=ft.Column(
                            controls=[
                                ft.ResponsiveRow( # O ResponsiveRow interno para as duas colunas de input
                                    columns=12, # Grid de 12 colunas
                                    spacing=50, 
                                    vertical_alignment=ft.CrossAxisAlignment.START, 
                                    controls=[
                                        # Coluna Esquerda: Nome, Número, Partido
                                        ft.Container(
                                            col={"xs": 12, "md": 6}, # Em telas pequenas, ocupa 12 colunas; em médias e maiores, 6.
                                            expand=True, 
                                            content=ft.Column(
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Text("Governador", size=70, weight="bold", color="black"), # Alterado o texto
                                                        alignment=ft.alignment.center_left,
                                                        margin=ft.Margin(left=0, top=0, right=0, bottom=10),
                                                    ),
                                                    styled_textfield(nome, "Ex: Maria de Souza", "Nome:"), # Alterado o hint_text
                                                    styled_textfield(numero, "Ex: 45", "Número:"), # Alterado o hint_text
                                                    styled_dropdown(partido_dropdown, dropdown_items, "Selecione o partido", "Partido:"),
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                                expand=True, 
                                            ),
                                            alignment=ft.alignment.top_left
                                        ),
                                        # Coluna Direita: Foto, Descrição, Botões
                                        ft.Container(
                                            col={"xs": 12, "md": 6}, # Em telas pequenas, ocupa 12 colunas; em médias e maiores, 6.
                                            expand=True, 
                                            content=ft.Column(
                                                controls=[
                                                    ft.Container(height=30), # Espaçamento
                                                    ft.Row( 
                                                        controls=[
                                                            ft.Text("Foto:", size=22, weight="bold", color="black"),
                                                            ft.Container(width=10), 
                                                            ft.Column(
                                                                controls=[
                                                                    imagem_preview_container,
                                                                    ft.Container(
                                                                        content=ft.Text("Selecionar imagem", size=14, color="black"),
                                                                        alignment=ft.alignment.center,
                                                                        width=150, 
                                                                        height=40,
                                                                        bgcolor="#DFEDFF",
                                                                        border=ft.border.all(1, "black"),
                                                                        ink=True,
                                                                        on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png", "gif"]),
                                                                        shadow=ft.BoxShadow(
                                                                            spread_radius=0, blur_radius=0, color="black", offset=ft.Offset(5, 5) 
                                                                        )
                                                                    ),
                                                                ]
                                                            )
                                                        ],
                                                        vertical_alignment=ft.CrossAxisAlignment.START, 
                                                    ),
                                                    ft.Container(height=20),
                                                    ft.Column( 
                                                        controls=[
                                                            ft.Text("Descrição:", size=22, weight="bold", color="black"),
                                                            ft.TextField(
                                                                ref=descricao,
                                                                color="black",
                                                                bgcolor="#DFEDFF",
                                                                multiline=True,
                                                                min_lines=4, 
                                                                max_lines=8, 
                                                                content_padding=ft.Padding(top=15, bottom=15, left=16, right=16),
                                                                border_radius=ft.border_radius.all(10),
                                                                label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
                                                                border_color="black", 
                                                                border_width=1,
                                                                expand=True, 
                                                            ),
                                                        ],
                                                        horizontal_alignment=ft.CrossAxisAlignment.START, 
                                                        expand=True, 
                                                    ),
                                                    ft.Container(height=10),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Container(
                                                                content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                                alignment=ft.alignment.center,
                                                                width=200, 
                                                                height=50,
                                                                bgcolor="#DFEDFF",
                                                                border=ft.border.all(1, "black"),
                                                                ink=True,
                                                                on_click=cadastrar_governador, # Alterado a função de clique
                                                                shadow=ft.BoxShadow(
                                                                    spread_radius=0, blur_radius=0, color="black", offset=ft.Offset(8, 8) 
                                                                ),
                                                            ),
                                                        ],
                                                        alignment=ft.MainAxisAlignment.START, 
                                                        expand=True, 
                                                    ),
                                                    ft.Container(height=10),
                                                    mensagem,
                                                ],
                                                horizontal_alignment=ft.CrossAxisAlignment.START, 
                                                spacing=0, 
                                                expand=True, 
                                            ),
                                            alignment=ft.alignment.top_left 
                                        ),
                                    ],
                                ),
                                # Botão "Voltar" fora do ResponsiveRow
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                "← Voltar",
                                                on_click=lambda e: e.page.go("/admin_painel_cadastro"), # Manter ou ajustar a rota de retorno
                                                style=ft.ButtonStyle(
                                                    color="black",
                                                    overlay_color="transparent",
                                                    text_style=ft.TextStyle(size=14)
                                                )
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.END, 
                                        expand=True,
                                    ),
                                    margin=ft.Margin(left=0, top=20, right=0, bottom=0) 
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                            alignment=ft.MainAxisAlignment.START, 
                            expand=True,
                            scroll=ft.ScrollMode.ADAPTIVE # Mantido para rolagem em telas pequenas
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER, # Centraliza o ResponsiveRow dentro do View
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True # Permite que este ResponsiveRow ocupe o espaço total do View
            )
        ]
    )