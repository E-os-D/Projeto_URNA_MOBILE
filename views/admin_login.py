import flet as ft
import sqlite3

def admin_login_view():
    email = ft.TextField(
        label="Digite seu email:",
        width=800,
        bgcolor="#FCF8EC",
        color="#000000",
        label_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
        border_radius=ft.border_radius.all(50),
        content_padding=ft.Padding(top=22, bottom=22, left=16, right=16)
    )

    senha = ft.TextField(
        label="Digite sua senha:",
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
                                                    content=ft.Text("Login Administrador", size=32, weight="bold"),
                                                    padding=ft.padding.only(bottom=50)
                                                ),
                                                ft.Column([
                                                    ft.Container(
                                                        content=ft.Text("E-mail:", size=23, weight="bold"),
                                                        alignment=ft.alignment.top_left,
                                                        padding=ft.padding.only(left=20, bottom=10)
                                                    ),
                                                    email,
                                                    ft.Container(height=20)
                                                ]),
                                                ft.Column([
                                                    ft.Container(
                                                        content=ft.Text("Senha:", size=23, weight="bold"),
                                                        alignment=ft.alignment.top_left,
                                                        padding=ft.padding.only(left=20, bottom=10)
                                                    ),
                                                    senha
                                                ]),
                                                mensagem,
                                                ft.Container(height=20),
                                                ft.Container(
                                                    content=ft.Text("ENTRAR", size=16, weight="bold", color="black"),
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
                                                            on_click=lambda _: _.page.go("/"),
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
