import flet as ft

def admin_painel_view():
    return ft.View(
        route="/admin_painel",
        controls=[
            ft.Text("Painel do Administrador", size=24, weight="bold"),
            ft.ElevatedButton("Cadastrar Candidato", on_click=lambda _: _.page.go("/cadastro_candidato")),
            ft.ElevatedButton("Cadastrar Admin", on_click=lambda _: _.page.go("/cadastro_admin")),
            ft.ElevatedButton("Visualizar Gráficos", on_click=lambda _: _.page.go("/graficos")),
            ft.ElevatedButton("Gerar Relatório TXT", on_click=lambda _: print("Relatório gerado!")),
            ft.TextButton("Voltar", on_click=lambda _: _.page.go("/"))
        ]
    )