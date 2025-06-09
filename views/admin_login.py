import flet as ft

def admin_login_view():
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)

    def login(e):
        # Simula login (substituir com validação real)
        if email.value == "admin" and senha.value == "123":
            e.page.go("/admin_panel")

    return ft.View(
        route="/admin_login",
        controls=[
            ft.Column([
                ft.Text("Login Administrador", size=24, weight="bold"),
                email,
                senha,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Voltar", on_click=lambda _: _.page.go("/"))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ]
    )