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
            snackbar.open = True
            drop.options = [ft.dropdown.Option(str(id), nome) for id, nome in obter_governadores()]
            drop.value = None
            e.page.snackbar = snackbar
            e.page.update()
        else:
            snackbar.content = ft.Text("Selecione um governador.")
            snackbar.open = True
            e.page.snackbar = snackbar
            e.page.update()

    return ft.View(
        route="/remocao_governador",
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
                    ]
                )
            )
        ]
    )
