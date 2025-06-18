import flet as ft
import sqlite3

def obter_eleitores():
    """Busca todos os eleitores no SQLite."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT idRG, nome FROM Eleitor")
    registros = cursor.fetchall()
    conn.close()
    return registros

def excluir_eleitor(id_rg):
    """Remove o eleitor pelo RG."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Eleitor WHERE idRG = ?", (id_rg,))
    conn.commit()
    conn.close()

def remocao_eleitor_view():
    eleitores = obter_eleitores()
    drop = ft.Dropdown(
        label="Selecione o Eleitor",
        options=[ft.dropdown.Option(id_rg, nome) for id_rg, nome in eleitores],
        width=400
    )
    snackbar = ft.SnackBar(content=ft.Text(""))

    def on_deletar(e):
        if drop.value:
            excluir_eleitor(drop.value)
            snackbar.content = ft.Text("Eleitor removido com sucesso.")
            snackbar.open = True
            drop.options = [ft.dropdown.Option(id_rg, nome) for id_rg, nome in obter_eleitores()]
            drop.value = None
            e.page.snackbar = snackbar
            e.page.update()
        else:
            snackbar.content = ft.Text("Selecione um eleitor.")
            snackbar.open = True
            e.page.snackbar = snackbar
            e.page.update()

    return ft.View(
        route="/remocao_eleitor",
        bgcolor="#ECCAD8",
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
                            height=580,
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
                                controls=[
                                    ft.Text(
                                        "Qual eleitor deseja remover?",
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
                    ]
                )
            )
        ]
    )
