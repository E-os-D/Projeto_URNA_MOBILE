import flet as ft
import sqlite3

def obter_partidos():
    """Busca todos os partidos no SQLite."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_partido, nome FROM Partidos")
    registros = cursor.fetchall()
    conn.close()
    return registros

def partido_tem_vinculo(id_partido):
    """Verifica se o partido está vinculado a algum candidato."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()

    tabelas = [
        ("Presidente", "id_partido"),
        ("Governador", "id_partido"),
        ("Prefeito", "id_partido")
    ]

    for tabela, campo in tabelas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE {campo} = ?", (id_partido,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return True

    conn.close()
    return False

def excluir_partido(id_partido):
    """Remove o partido pelo ID."""
    conn = sqlite3.connect('urna_eletronica.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Partidos WHERE id_partido = ?", (id_partido,))
    conn.commit()
    conn.close()

def remocao_partido_view():
    partidos = obter_partidos()
    drop = ft.Dropdown(
        label="Selecione o Partido",
        options=[ft.dropdown.Option(str(id), nome) for id, nome in partidos],
        width=400
    )
    snackbar = ft.SnackBar(content=ft.Text(""))

    def on_deletar(e):
        if drop.value:
            id_partido = int(drop.value)
            if partido_tem_vinculo(id_partido):
                snackbar.content = ft.Text("Erro: Partido vinculado a um candidato.")
            else:
                excluir_partido(id_partido)
                snackbar.content = ft.Text("Partido removido com sucesso.")
                drop.options = [ft.dropdown.Option(str(id), nome) for id, nome in obter_partidos()]
                drop.value = None
            snackbar.open = True
            e.page.snackbar = snackbar
            e.page.update()
        else:
            snackbar.content = ft.Text("Selecione um partido.")
            snackbar.open = True
            e.page.snackbar = snackbar
            e.page.update()

    return ft.View(
        route="/remocao_partido",
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
                                "Qual partido deseja remover?",
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