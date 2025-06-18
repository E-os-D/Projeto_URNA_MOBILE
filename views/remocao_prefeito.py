import flet as ft
import sqlite3

def obter_prefeitos():
    """Busca todos os prefeitos no SQLite."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_número_prefeito, nome FROM Prefeito")
    registros = cursor.fetchall()
    conn.close()
    return registros

def excluir_prefeito(id_prefeito):
    """Remove o prefeito pelo ID."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Prefeito WHERE id_número_prefeito = ?", (id_prefeito,))
    conn.commit()
    conn.close()


def remocao_prefeito_view():
    prefeitos = obter_prefeitos()
    drop = ft.Dropdown(
        label="Selecione o Prefeito",
        options=[ft.dropdown.Option(str(id), nome) for id, nome in prefeitos],
        width=400
    )
    snackbar = ft.SnackBar(content=ft.Text(""))

    def on_deletar(e):
        if drop.value:
            excluir_prefeito(int(drop.value))
            snackbar.content = ft.Text("Prefeito removido com sucesso.")
            snackbar.open = True
            drop.options = [ft.dropdown.Option(str(id), nome) for id, nome in obter_prefeitos()]
            drop.value = None
            e.page.snackbar = snackbar
            e.page.update()
        else:
            snackbar.content = ft.Text("Selecione um prefeito.")
            snackbar.open = True
            e.page.snackbar = snackbar
            e.page.update()

    return ft.View(
        route="/remocao_prefeito",
        bgcolor="#FFE9C0",  # cor de fundo diferente para diferenciar
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
