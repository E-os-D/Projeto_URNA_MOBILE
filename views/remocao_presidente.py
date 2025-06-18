import flet as ft
import sqlite3

def obter_presidentes():
    """Busca todos os presidentes no SQLite."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_número_presidente, nome FROM Presidente")
    registros = cursor.fetchall()
    conn.close()
    return registros

def excluir_presidente(id_presidente):
    """Remove o presidente pelo ID."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Presidente WHERE id_número_presidente = ?", (id_presidente,))
    conn.commit()
    conn.close()

def remocao_presidente_view():
    presidentes = obter_presidentes()
    drop = ft.Dropdown(
        label="Selecione o Presidente",
        options=[ft.dropdown.Option(str(id), nome) for id, nome in presidentes],
        width=400
    )
    snackbar = ft.SnackBar(content=ft.Text(""))

    def on_deletar(e):
        if drop.value:
            excluir_presidente(int(drop.value))
            snackbar.content = ft.Text("Presidente removido com sucesso.")
            drop.options = [ft.dropdown.Option(str(id), nome) for id, nome in obter_presidentes()]
            drop.value = None
        else:
            snackbar.content = ft.Text("Selecione um presidente.")
        snackbar.open = True
        e.page.snackbar = snackbar
        e.page.update()

    return ft.View(
        route="/remocao_presidente",
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