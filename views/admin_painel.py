import flet as ft
import sqlite3
import os
from datetime import datetime # Para nomear o arquivo com data e hora

def admin_painel_view():
    def voltar(e):
        e.page.go("/")

    def ir_cadastrar(e):
        e.page.go("/admin_painel_cadastro")

    # A função ir_relatorio será modificada para gerar o TXT
    def ir_relatorio(e):
        # Gera um nome de arquivo único com a data e hora atual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_votacao_{timestamp}.txt"
        
        relatorio_conteudo = []
        relatorio_conteudo.append("--- RELATÓRIO DE VOTAÇÃO ---\n")
        relatorio_conteudo.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio_conteudo.append("------------------------------\n\n")

        conn = None # Inicializa conn como None
        try:
            conn = sqlite3.connect("urna_eletronica.db")
            cursor = conn.cursor()

            # --- Votos para Presidente ---
            relatorio_conteudo.append("--- RESULTADO PRESIDENTE ---\n")
            cursor.execute("SELECT id_número_presidente, nome, votos FROM Presidente ORDER BY votos DESC")
            presidentes = cursor.fetchall()
            if presidentes:
                for num, nome_pres, votos in presidentes:
                    relatorio_conteudo.append(f"Número: {num} | Nome: {nome_pres} | Votos: {votos}\n")
            else:
                relatorio_conteudo.append("Nenhum candidato a Presidente encontrado ou sem votos.\n")
            relatorio_conteudo.append("\n")

            # --- Votos para Governador ---
            relatorio_conteudo.append("--- RESULTADO GOVERNADOR ---\n")
            cursor.execute("SELECT id_número_governador, nome, votos FROM Governador ORDER BY votos DESC")
            governadores = cursor.fetchall()
            if governadores:
                for num, nome_gov, votos in governadores:
                    relatorio_conteudo.append(f"Número: {num} | Nome: {nome_gov} | Votos: {votos}\n")
            else:
                relatorio_conteudo.append("Nenhum candidato a Governador encontrado ou sem votos.\n")
            relatorio_conteudo.append("\n")
            
            # --- Votos Nulos e Brancos (exemplo, ajuste conforme seu DB) ---
            # Se você tiver uma tabela ou forma de registrar votos nulos/brancos
            relatorio_conteudo.append("--- OUTROS VOTOS ---\n")
            # Exemplo: Se você tiver uma tabela 'VotosGerais' ou similar
            # cursor.execute("SELECT tipo, total_votos FROM VotosGerais WHERE tipo IN ('NULOS', 'BRANCOS')")
            # outros_votos = cursor.fetchall()
            # for tipo, total in outros_votos:
            #     relatorio_conteudo.append(f"{tipo}: {total}\n")
            relatorio_conteudo.append("Nulos: (Ajustar consulta)\n")
            relatorio_conteudo.append("Brancos: (Ajustar consulta)\n")
            relatorio_conteudo.append("\n")

            # Salva o conteúdo no arquivo TXT
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.writelines(relatorio_conteudo)
            
            print(f"Relatório salvo em: {os.path.abspath(nome_arquivo)}")
            # Exibe uma mensagem de sucesso para o usuário
            e.page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(f"Relatório gerado com sucesso em '{nome_arquivo}'!"),
                    open=True,
                    bgcolor=ft.colors.GREEN_700
                )
            )

        except sqlite3.Error as sqle:
            error_message = f"Erro no banco de dados ao gerar relatório: {sqle}"
            print(error_message)
            e.page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(error_message),
                    open=True,
                    bgcolor=ft.colors.RED_700
                )
            )
        except Exception as ex:
            error_message = f"Erro inesperado ao gerar relatório: {ex}"
            print(error_message)
            e.page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(error_message),
                    open=True,
                    bgcolor=ft.colors.RED_700
                )
            )
        finally:
            if conn:
                conn.close()
        e.page.update()

    def ir_grafico(e):
        e.page.go("/graficos")

    def ir_remocao(e):
        e.page.go("/admin_remocao")

    # Linha 1 de ícones
    opcoes = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_candidatos.png", width=150),
                    ft.Container(
                        content=ft.Text("Cadastrar.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_cadastrar
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_relatorio.png", width=150),
                    ft.Container(
                        content=ft.Text("Relatório.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_relatorio # Chamará a função modificada
            )
        ],
        alignment="center",
        spacing=80
    )

    # Linha 2 de ícones
    opcoes2 = ft.Row(
        controls=[
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_grafico.png", width=150),
                    ft.Container(
                        content=ft.Text("Gráfico.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_grafico
            ),
            ft.GestureDetector(
                content=ft.Column([
                    ft.Image(src="img/admin_administrador.png", width=150),
                    ft.Container(
                        content=ft.Text("Remoção.", size=20),
                        alignment=ft.alignment.center_right,
                        width=150
                    )
                ], horizontal_alignment="center"),
                on_tap=ir_remocao
            )
        ],
        alignment="center",
        spacing=80
    )

    # Botão de voltar no canto inferior direito
    voltar_row = ft.Row(
        [ft.TextButton(
            "← Voltar",
            on_click=voltar,
            style=ft.ButtonStyle(color="black")
        )],
        alignment="end"
    )

    return ft.View(
        route="/admin_painel",
        bgcolor="#FCF8EC",
        padding=20,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                                        padding=70,
                                        bgcolor="white",
                                        border=ft.border.all(width=1, color="black"),
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=0,
                                            color="black",
                                            offset=ft.Offset(15, 15)
                                        ),
                                        content=ft.Column(
                                            scroll=ft.ScrollMode.AUTO,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(  # Centro dos ícones
                                                    content=ft.Column(
                                                        [opcoes, opcoes2],
                                                        spacing=50,
                                                        alignment="center"
                                                    ),
                                                    expand=True,
                                                    alignment=ft.alignment.center
                                                ),
                                                voltar_row  # Botão no fim
                                            ],
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )