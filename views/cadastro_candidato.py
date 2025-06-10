import flet as ft

def cadastro_candidato_view():
    return ft.View(
        route="/cadastro_candidato",
        controls=[
            ft.Text("Cadastro de Candidato", size=22, weight="bold"),
            ft.TextField(label="Nome"),
            ft.TextField(label="Número"),
            ft.TextField(label="Partido"),
            ft.TextField(label="Cargo"),
            ft.TextField(label="Descrição"),
            ft.ElevatedButton("Salvar"),
            ft.TextButton("Voltar", on_click=lambda _: _.page.go("/admin_painel"))
        ]
    )