import flet as ft
import sqlite3

def buscar_candidatos(cargo):
    conn = sqlite3.connect("urna_eletronica.db")
    cur = conn.cursor()

    campo_numero = f"id_número_{cargo.lower()}"
    cur.execute(f"SELECT {campo_numero}, nome, foto FROM {cargo}")
    candidatos = cur.fetchall()
    conn.close()
    return candidatos


def registrar_voto(cargo, numero):
    conn = sqlite3.connect("urna_eletronica.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO Votação_{cargo.lower()} (numero) VALUES (?)", (numero,))
    conn.commit()
    conn.close()

def proximo_cargo(cargo):
    ordem = ["Presidente", "Governador", "Prefeito"]
    if cargo in ordem:
        i = ordem.index(cargo)
        return f"/votacao_{ordem[i+1].lower()}" if i + 1 < len(ordem) else "/resultado"
    return "/"

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
        registrar_voto(cargo, "branco")
        e.page.go(proximo_cargo(cargo))

    def confirmar(e):
        if numero_digitado.value:
            registrar_voto(cargo, numero_digitado.value)
            e.page.go(proximo_cargo(cargo))

    # Teclado numérico
    teclado = ft.Column(
        controls=[
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=50) for i in range(1, 4)]),
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=50) for i in range(4, 7)]),
            ft.Row([ft.ElevatedButton(text=str(i), on_click=preencher, width=50) for i in range(7, 10)]),
            ft.Row([ft.ElevatedButton(text="0", on_click=preencher, width=50)]),
            ft.Row([
                ft.ElevatedButton("Branco", on_click=branco),
                ft.ElevatedButton("Corrige", on_click=corrigir),
                ft.ElevatedButton("Confirma", on_click=confirmar)
            ])
        ]
    )

    # Lista de candidatos com imagem
    candidatos = buscar_candidatos(cargo)
    candidatos_cards = [
        ft.Column([
            ft.Image(src=f"img/{foto}", width=120),
            ft.Text(f"{nome} - Nº {numero}", size=16)
        ], horizontal_alignment="center")
        for numero, nome, foto in candidatos
    ]

    return ft.View(
        route=f"/votacao_{cargo.lower()}",
        bgcolor="#FCF8EC",
        controls=[
            ft.Text(f"Votação para {cargo}", size=24),
            ft.Divider(),
            ft.Row(candidatos_cards, alignment="center", wrap=True),
            ft.Row([numero_digitado], alignment="center"),
            ft.Row([teclado], alignment="center")
        ]
    )

def proxima_votacao(atual):
    ordem = ["Presidente", "Governador", "Prefeito"]
    try:
        index = ordem.index(atual)
        return ordem[index + 1]
    except (ValueError, IndexError):
        return None  # Fim da votação

