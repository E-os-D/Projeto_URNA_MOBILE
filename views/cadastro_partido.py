import flet as ft
import sqlite3

def cadastro_partido_view():
    nome = ft.TextField(
        label="Nome",
        width=800, 
        bgcolor="#DFEDFF", 
        color="#000000", 
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
    )
    numero = ft.TextField(
        label="Número",
        password=True,
        width=800, 
        bgcolor="#DFEDFF", 
        color="#000000", 
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
        )
    sigla = ft.TextField(
        label="Sigla", 
        password=True,
        width=800, 
        bgcolor="#DFEDFF", 
        color="#000000", 
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
        )

    mensagem = ft.Text("", color="red")
    
    def login(e):
        conn = sqlite3.connect("urna_eletronica.db")
        cursor = conn.cursor()

        # Verifica se o partido já está cadastrado
        cursor.execute("SELECT * FROM Partidos WHERE id_partido = ?", (numero.value,))
        usuario = cursor.fetchone()

        if usuario:
            mensagem.value = "Partido já cadastrado."
        else:
            if nome.value.strip() == "" or numero.value.strip() == "" or sigla.value.strip() == "":
                mensagem.value = "Preencha todos os campos."
            else:
                # Cadastra o partido
                cursor.execute("INSERT INTO Partidos (nome, id_partido, sigla) VALUES (?, ?, ?)",
                            (nome.value, numero.value, sigla.value))
                conn.commit()
                mensagem.value = "Partido cadastrado com sucesso!"
                # Limpa os campos
                nome.value = ""
                numero.value = ""
                sigla.value = ""

        conn.close()
        e.page.update()
    
    return ft.View(
        route="/cadastro_partido",
        bgcolor="#D3E5FD",
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
                                        padding=40,
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
                                                ft.Container(
                                                    content=ft.Text("Cadastro de Partido", size=32, weight="bold"),
                                                    padding=ft.padding.only(bottom=50)
                                                ),
                                                #NOME
                                                ft.Column([
                                                    ft.Container(
                                                        content=ft.Text("Nome:", size=23, weight="bold"),
                                                        alignment=ft.alignment.top_left,
                                                        padding=ft.padding.only(left=20, bottom=10)
                                                    ),
                                                    nome,
                                                    ft.Container(height=20)
                                                ]),
                                                #Número
                                                ft.Column([
                                                    ft.Container(
                                                        content=ft.Text("Número:", size=23, weight="bold"),
                                                        alignment=ft.alignment.top_left,
                                                        padding=ft.padding.only(left=20, bottom=10)
                                                    ),
                                                    numero
                                                ]),
                                                #SIGLA
                                                ft.Column([
                                                    ft.Container(
                                                        content=ft.Text("Sigla:", size=23, weight="bold"),
                                                        alignment=ft.alignment.top_left,
                                                        padding=ft.padding.only(left=20, bottom=10)
                                                    ),
                                                    sigla
                                                ]),
                                                mensagem,
                                                ft.Container(height=20),
                                                ft.Container(
                                                    content=ft.Text("CADASTRAR", size=16, weight="bold", color="black"),
                                                    alignment=ft.alignment.center,
                                                    width=150,
                                                    height=50,
                                                    bgcolor="#FCF8EC",
                                                    border=ft.border.all(1, "black"),
                                                    margin=ft.margin.only(top=5, left=5),
                                                    ink=True,
                                                    on_click=login,
                                                    shadow=ft.BoxShadow(
                                                        spread_radius=0,
                                                        blur_radius=0,
                                                        color="black",
                                                        offset=ft.Offset(5, 5)
                                                    )
                                                ),
                                                ft.Container(height=20),
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.END,
                                                    controls=[
                                                        ft.TextButton(
                                                            "← Voltar",
                                                            on_click=lambda _: _.page.go("/admin_painel_cadastro"),
                                                            style=ft.ButtonStyle(color="black")
                                                        )
                                                    ]
                                                )
                                            ]
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