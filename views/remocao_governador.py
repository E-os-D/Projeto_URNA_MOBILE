import flet as ft
import sqlite3

def obter_governadores():
    """Busca todos os governadores no SQLite."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_número_governador, nome FROM Governador")
    registros = cursor.fetchall()
    conn.close()
    return registros

def excluir_governador(id_governador):
    """Remove o governador pelo ID."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Governador WHERE id_número_governador = ?", (id_governador,))
    conn.commit()
    conn.close()


def remocao_governador_view():
    governadores = obter_governadores()
    drop = ft.Dropdown(
        label="Selecione o Governador",
        options=[ft.dropdown.Option(str(id), nome) for id, nome in governadores],
        width=400
    )
    snackbar = ft.SnackBar(content=ft.Text(""))

    def on_deletar(e):
        if drop.value:
            excluir_governador(int(drop.value))
            snackbar.content = ft.Text("Governador removido com sucesso.")
            drop.options = [ft.dropdown.Option(str(id), nome) for id, nome in obter_governadores()]
            drop.value = None
        else:
            snackbar.content = ft.Text("Selecione um governador.")

        snackbar.open = True
        e.page.snackbar = snackbar
        e.page.update()

    return ft.View(
        route="/remocao_governador",
        bgcolor="#ECCAD8",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=500,
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
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        tight=True,
                        controls=[
                            ft.Text(
                                "Quem deseja remover?",
                                size=24,
                                weight=ft.FontWeight.W_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            drop,
                            ft.ElevatedButton(text="Deletar", on_click=on_deletar),
                            snackbar,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.TextButton(
                                        "← Voltar.",
                                        style=ft.ButtonStyle(color="black"),
                                        on_click=lambda e: e.page.go("/remocao_painel")
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        ]
    )