import flet as ft

def resultado_view():
    return ft.View(
        route="/resultado",
        controls=[
            ft.Text("Voto finalizado! Obrigado por participar.", size=20),
            ft.TextButton("Voltar à tela inicial", on_click=lambda _: _.page.go("/"))
        ]
    )