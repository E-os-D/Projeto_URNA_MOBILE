import flet as ft
import sqlite3

def registrar_voto(cargo, numero):
    try:
        campo = f"id_número_{cargo.lower()}"
        with sqlite3.connect("urna_eletronica.db") as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Votação_{cargo.lower()} ({campo}) VALUES (?)", (numero,))
            conn.commit()
    except Exception as e:
        print(f"Erro ao registrar voto: {e}")

def proxima_votacao(atual):
    ordem = ["Presidente", "Governador", "Prefeito"]
    try:
        index = ordem.index(atual)
        return ordem[index + 1]
    except (ValueError, IndexError):
        return None

def votacao_view(cargo):
    numero_digitado = ft.TextField(label="Número:", width=200, read_only=True)

    def preencher(e):
        if len(numero_digitado.value) < 2:
            numero_digitado.value += e.control.text
            numero_digitado.update()

    def corrigir(e):
        numero_digitado.value = ""
        numero_digitado.update()

    def branco(e):
        registrar_voto(cargo, 0)
        proximo = proxima_votacao(cargo)
        if proximo:
            e.page.go(f"/votacao_{proximo.lower()}")
        else:
            e.page.go("/fim")

    def confirmar(e):
        if numero_digitado.value:
            registrar_voto(cargo, int(numero_digitado.value))
            proximo = proxima_votacao(cargo)
            if proximo:
                e.page.go(f"/votacao_{proximo.lower()}")
            else:
                e.page.go("/fim")

    teclado = ft.Column(
        controls=[
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=60) for i in range(1, 4)]),
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=60) for i in range(4, 7)]),
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=60) for i in range(7, 10)]),
            ft.Row([ft.ElevatedButton(text="0", on_click=preencher, width=60)]),
            ft.Row([
                ft.ElevatedButton("Branco", on_click=branco, bgcolor="white", color="black"),
                ft.ElevatedButton("Corrigir", on_click=corrigir, bgcolor="orange"),
                ft.ElevatedButton("Confirmar", on_click=confirmar, bgcolor="green", color="white")
            ], alignment="center")
        ]
    )

    return ft.View(
        route=f"/votacao_{cargo.lower()}",
        controls=[
            ft.Text(f"Votação para {cargo}", size=26, weight="bold"),
            numero_digitado,
            teclado
        ]
    )