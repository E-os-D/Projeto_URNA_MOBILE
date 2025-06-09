import flet as ft

def cadastro_admin_view():
    return ft.View(
        route="/cadastro_admin",
        controls=[
            ft.Text("Cadastro de Admin", size=22, weight="bold"),
            ft.TextField(label="Nome"),
            ft.TextField(label="Email"),
            ft.TextField(label="Senha", password=True),
            ft.ElevatedButton("Cadastrar"),
            ft.TextButton("Voltar", on_click=lambda _: _.page.go("/admin_panel"))
        ]
    )