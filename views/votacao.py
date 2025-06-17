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
    numero_digitado = ft.TextField(
        label="Número do candidato",
        width=200,
        read_only=True,
        text_align=ft.TextAlign.CENTER
    )

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
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row([ft.ElevatedButton(str(i), on_click=preencher, width=80, height=60) for i in range(1, 4)], alignment="center"),
            ft.Row([ft.ElevatedButton(str(i), on_click=preencher, width=80, height=60) for i in range(4, 7)], alignment="center"),
            ft.Row([ft.ElevatedButton(str(i), on_click=preencher, width=80, height=60) for i in range(7, 10)], alignment="center"),
            ft.Row([ft.ElevatedButton("0", on_click=preencher, width=80, height=60)], alignment="center"),
            ft.Row([
                ft.ElevatedButton("Branco", on_click=branco, bgcolor="white", color="black", width=100),
                ft.ElevatedButton("Corrigir", on_click=corrigir, bgcolor="orange", width=100),
                ft.ElevatedButton("Confirmar", on_click=confirmar, bgcolor="green", color="white", width=100)
            ], alignment="center")
        ]
    )

    return ft.View(
        route=f"/votacao_{cargo.lower()}",
        bgcolor="#FCF8EC",
        padding=20,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 10, "lg": 8, "xl": 6},
                            height=600,
                            padding=30,
                            bgcolor="white",
                            border=ft.border.all(1, "black"),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=0,
                                color="black",
                                offset=ft.Offset(15, 15)
                            ),
                            content=ft.Column(
                                spacing=25,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        f"Votação para {cargo}",
                                        size=24,
                                        weight=ft.FontWeight.W_600,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    numero_digitado,
                                    teclado,
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        controls=[
                                            ft.TextButton(
                                                "← Sair da votação",
                                                style=ft.ButtonStyle(color="black"),
                                                on_click=lambda e: e.page.go("/")
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )
