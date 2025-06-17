import flet as ft
import sqlite3

def buscar_candidatos(cargo):
    conn = sqlite3.connect("urna_eletronica.db")
    cur = conn.cursor()

    campo_numero = f"id_número_{cargo.lower()}"  # corrigido (sem acento!)
    try:
        cur.execute(f"""
            SELECT c.{campo_numero}, c.nome, c.foto, c.descricao, p.nome AS partido, p.sigla
            FROM {cargo} AS c
            LEFT JOIN Partidos AS p ON c.id_partido = p.id_partido
        """)
        candidatos = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar candidatos: {e}")
        candidatos = []
    conn.close()
    return candidatos

def registrar_voto(cargo, numero):
    conn = sqlite3.connect("urna_eletronica.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO Votação_{cargo.lower()} (numero) VALUES (?)", (numero,))
    conn.commit()
    conn.close()

def proxima_votacao(atual):
    ordem = ["Presidente", "Governador", "Prefeito"]
    try:
        index = ordem.index(atual)
        return ordem[index + 1]
    except (ValueError, IndexError):
        return None  # Fim da votação

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
        proximo = proxima_votacao(cargo)
        if proximo:
            e.page.go(f"/Votação_{proximo.lower()}")
        else:
            e.page.go("/fim")

    def confirmar(e):
        if numero_digitado.value:
            registrar_voto(cargo, numero_digitado.value)
            proximo = proxima_votacao(cargo)
            if proximo:
                e.page.go(f"/Votação_{proximo.lower()}")
            else:
                e.page.go("/fim")

    # Teclado numérico
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

    # Cards de candidatos
    candidatos = buscar_candidatos(cargo)
    cards = []
    for numero, nome, foto, descricao, partido, sigla in candidatos:
        card = ft.Card(
            elevation=2,
            content=ft.Container(
                padding=10,
                width=200,
                bgcolor="#FFFFFF",
                content=ft.Column(
                    controls=[
                        ft.Image(src=f"img/{foto}", width=180, height=140, fit="cover"),
                        ft.Text(f"{nome} - {sigla} - Nº {numero}", size=16, weight="bold"),
                        ft.Text(f"Partido: {partido}", size=14),
                        ft.Text(descricao, size=12, italic=True)
                    ],
                    horizontal_alignment="center"
                )
            )
        )
        cards.append(card)

    return ft.View(
        route=f"/Votação_{cargo.lower()}",
        bgcolor="#FCF8EC",
        padding=20,
        controls=[
            ft.Text(f"Votação {cargo}", size=26, weight="bold"),
            ft.Divider(),
            ft.ResponsiveRow(cards, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                margin=20,
                content=ft.Column([
                    ft.Row([numero_digitado], alignment="center"),
                    ft.Row([teclado], alignment="center")
                ])
            )
        ]
    )