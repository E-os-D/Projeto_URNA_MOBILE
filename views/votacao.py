import flet as ft

def votacao_view(cargo):
    return ft.View(
        route=f"/votacao_{cargo.lower()}",
        controls=[
            ft.Text(f"Votar para {cargo}", size=24, weight="bold"),
            ft.TextField(label="Digite o número do candidato"),
            ft.Row([
                ft.ElevatedButton("Corrige"),
                ft.ElevatedButton("Confirma", on_click=lambda _: _.page.go(proxima_votacao(cargo)))
            ]),
        ]
    )

def proxima_votacao(cargo):
    if cargo == "Presidente":
        return "/votacao_governador"
    elif cargo == "Governador":
        return "/votacao_prefeito"
    else:
        return "/resultado"