import flet as ft
import sqlite3

def eleitor_login_view():
    nome = ft.TextField(label="Nome")
    rg = ft.TextField(label="RG")
    mensagem = ft.Text("", color="red")

    def login(e):
        conn = sqlite3.connect("urna_eletronica.db")
        cursor = conn.cursor()

        # Verifica se o eleitor já está cadastrado (ou seja, já votou)
        cursor.execute("SELECT * FROM Eleitor WHERE nome = ? AND rg = ?", (nome.value, rg.value))
        usuario = cursor.fetchone()

        if usuario:
            mensagem.value = "Eleitor já votou."
            e.page.update()
        else:
            # Cadastra o eleitor e permite votar
            cursor.execute("INSERT INTO Eleitor (nome, rg) VALUES (?, ?)", (nome.value, rg.value))
            conn.commit()
            e.page.go("/votacao_presidente")

        conn.close()

    return ft.View(
        route="/eleitor_login",
        controls=[
            ft.Column([
                nome,
                rg,
                mensagem,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Voltar", on_click=lambda _: _.page.go("/"))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ]
    )
