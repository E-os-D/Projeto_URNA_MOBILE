import flet as ft

def graficos_view():
    return ft.View(
        route="/graficos",
        controls=[
            ft.Text("Gráfico de Votações", size=22, weight="bold"),
            ft.Text("(gráfico real deve ser implementado usando flet.chart ou gráfico customizado)", size=12, italic=True),
            ft.TextButton("Voltar", on_click=lambda _: _.page.go("/admin_panel"))
        ]
    )