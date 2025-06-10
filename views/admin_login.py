import flet as ft
import sqlite3

def admin_login_view():
    email = ft.TextField(
        label= "Digite seu email:",
        width=800, 
        bgcolor="#FCF8EC", 
        color="#000000", 
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
    )
    senha = ft.TextField(
        label= "Digite sua senha:",
        password=True,
        width=800,
        bgcolor="#FCF8EC",
        color="#000000",
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
    )

    mensagem = ft.Text("", color="red")

    def login(e):
        conn = sqlite3.connect("urna_eletronica.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin WHERE email = ? AND senha = ?", (email.value, senha.value))
        usuario = cursor.fetchone()

        if usuario:
            e.page.go("/admin_painel")
        else:
            mensagem.value = "Email ou senha inválidos!"
            e.page.update()

        conn.close()

    return ft.View(
        route="/admin_login",
        bgcolor="#FCF8EC",
        controls=[
            ft.Stack(
                controls=[
                    ft.Container(
                        width=1700,
                        height=840,
                        bgcolor="black",
                        margin=ft.Margin(70, 70, 0, 0),
                    ),
                    ft.Container(
                        width=1700,
                        height=850,
                        bgcolor="white",
                        border=ft.border.all(width=1, color="black"),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Login Administrador", size=32, weight="bold"),
                                            margin=ft.margin.only(bottom=100),
                                            alignment=ft.alignment.center
                                        ),

                                        # EMAIL
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Container(
                                                    content=ft.Text("E-mail:", size=23, weight="bold"),
                                                    alignment=ft.alignment.top_left,
                                                    margin=ft.Margin(470, 0, 0, 0)  # left, top, right, bottom
                                                ),
                                                ft.Container(content=email, margin=ft.margin.only(bottom=30)),
                                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                        ), 

                                        # SENHA
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Container(
                                                    content=ft.Text("Senha:", size=23, weight="bold"),
                                                    alignment=ft.alignment.top_left,
                                                    margin=ft.Margin(470, 0, 0, 0)  # left, top, right, bottom
                                                ),
                                                senha
                                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,)
                                        ),

                                        mensagem,

                                        ft.ElevatedButton("Entrar", on_click=login),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    expand=True
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.TextButton(
                                            "← Voltar",
                                            on_click=lambda _: _.page.go("/"),
                                            style=ft.ButtonStyle(
                                                color="black",
                                            )
                                        )
                                    ]
                                ),
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                ],
                expand=True,
                alignment=ft.alignment.center,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
