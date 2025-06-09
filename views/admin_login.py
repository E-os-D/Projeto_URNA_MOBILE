import flet as ft
import sqlite3

def admin_login_view():
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)
    mensagem = ft.Text("", color="red")

    def login(e):
        conn = sqlite3.connect("urna_eletronica.db")
        cursor = conn.cursor()

        # Verifica se existe usuário com esse email e senha
        cursor.execute("SELECT * FROM Admin WHERE email = ? AND senha = ?", (email.value, senha.value))
        usuario = cursor.fetchone()

        if usuario:
            e.page.go("/admin_panel")
        else:
            mensagem.value = "Email ou senha inválidos!"
            e.page.update()

        conn.close()

    return ft.View(
        route="/admin_login",
        controls=[
            ft.Column([
                ft.Text("Login Administrador", size=24, weight="bold"),
                email,
                senha,
                mensagem,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Voltar", on_click=lambda _: _.page.go("/"))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ]
    )