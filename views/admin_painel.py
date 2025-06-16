import flet as ft
import sqlite3
import os
from datetime import datetime

# Função para estabelecer conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("urna_eletronica.db")
    # Configura o row_factory para acessar colunas por nome
    conn.row_factory = sqlite3.Row
    return conn

def admin_painel_view():
    def voltar(e):
        e.page.go("/")

    def ir_cadastrar(e):
        e.page.go("/admin_painel_cadastro")

    # A função ir_relatorio voltou a ser síncrona
    def ir_relatorio(e: ft.ControlEvent): # A função não é mais assíncrona
        conn = None # Inicializa conn como None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_votacao_{timestamp}.txt" # Salva no diretório atual
            
            relatorio_conteudo = []
            relatorio_conteudo.append("--- RELATÓRIO DE VOTAÇÃO ---\n")
            relatorio_conteudo.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            relatorio_conteudo.append("------------------------------\n\n")

            conn = get_db_connection()
            cursor = conn.cursor()

            # Função auxiliar para obter o nome do partido dado o ID
            def get_party_name(party_id):
                if party_id is None:
                    return "Não Informado" # Caso o id_partido seja nulo
                cursor.execute("SELECT nome FROM Partidos WHERE id_partido = ?", (party_id,))
                result = cursor.fetchone()
                return result['nome'] if result else "Partido Desconhecido"

            # --- Votos para Presidente ---
            relatorio_conteudo.append("--- RESULTADO PRESIDENTE ---\n")
            cursor.execute("""
                SELECT
                    p.id_número_presidente,
                    p.nome,
                    p.id_partido,
                    COUNT(vp.idvotos) AS total_votos
                FROM
                    Presidente AS p
                LEFT JOIN
                    Votação_presidente AS vp ON p.id_número_presidente = vp.id_número_presidente
                GROUP BY
                    p.id_número_presidente, p.nome, p.id_partido
                ORDER BY
                    total_votos DESC;
            """)
            presidentes = cursor.fetchall()
            
            if presidentes:
                # Encontra o ganhador (o primeiro da lista ordenada)
                winner_pres = presidentes[0]
                party_name_pres = get_party_name(winner_pres['id_partido'])
                relatorio_conteudo.append(f"GANHADOR: {winner_pres['nome']} | PARTIDO: {party_name_pres} | NÚMERO: {winner_pres['id_número_presidente']}\n")
                relatorio_conteudo.append("----------------------------------\n")
                for row in presidentes:
                    relatorio_conteudo.append(f"Número: {row['id_número_presidente']} | Nome: {row['nome']} | Votos: {row['total_votos']}\n")
            else:
                relatorio_conteudo.append("Nenhum candidato a Presidente encontrado ou sem votos.\n")
            relatorio_conteudo.append("\n")

            # --- Votos para Governador ---
            relatorio_conteudo.append("--- RESULTADO GOVERNADOR ---\n")
            cursor.execute("""
                SELECT
                    g.id_número_governador,
                    g.nome,
                    g.id_partido,
                    COUNT(vg.idvotos) AS total_votos
                FROM
                    Governador AS g
                LEFT JOIN
                    Votação_governador AS vg ON g.id_número_governador = vg.id_número_governador
                GROUP BY
                    g.id_número_governador, g.nome, g.id_partido
                ORDER BY
                    total_votos DESC;
            """)
            governadores = cursor.fetchall()
            if governadores:
                # Encontra o ganhador
                winner_gov = governadores[0]
                party_name_gov = get_party_name(winner_gov['id_partido'])
                relatorio_conteudo.append(f"GANHADOR: {winner_gov['nome']} | PARTIDO: {party_name_gov} | NÚMERO: {winner_gov['id_número_governador']}\n")
                relatorio_conteudo.append("----------------------------------\n")
                for row in governadores:
                    relatorio_conteudo.append(f"Número: {row['id_número_governador']} | Nome: {row['nome']} | Votos: {row['total_votos']}\n")
            else:
                relatorio_conteudo.append("Nenhum candidato a Governador encontrado ou sem votos.\n")
            relatorio_conteudo.append("\n")

            # --- Votos para Prefeito ---
            relatorio_conteudo.append("--- RESULTADO PREFEITO ---\n")
            cursor.execute("""
                SELECT
                    pf.id_número_prefeito,
                    pf.nome,
                    pf.id_partido,
                    COUNT(vpf.idvotos) AS total_votos
                FROM
                    Prefeito AS pf
                LEFT JOIN
                    Votação_prefeito AS vpf ON pf.id_número_prefeito = vpf.id_número_prefeito
                GROUP BY
                    pf.id_número_prefeito, pf.nome, pf.id_partido
                ORDER BY
                    total_votos DESC;
            """)
            prefeitos = cursor.fetchall()
            if prefeitos:
                # Encontra o ganhador
                winner_pref = prefeitos[0]
                party_name_pref = get_party_name(winner_pref['id_partido'])
                relatorio_conteudo.append(f"GANHADOR: {winner_pref['nome']} | PARTIDO: {party_name_pref} | NÚMERO: {winner_pref['id_número_prefeito']}\n")
                relatorio_conteudo.append("----------------------------------\n")
                for row in prefeitos:
                    relatorio_conteudo.append(f"Número: {row['id_número_prefeito']} | Nome: {row['nome']} | Votos: {row['total_votos']}\n")
            else:
                relatorio_conteudo.append("Nenhum candidato a Prefeito encontrado ou sem votos.\n")
            relatorio_conteudo.append("\n")

            # --- Votos Nulos e Brancos (exemplo, ajuste conforme seu DB) ---
            relatorio_conteudo.append("--- OUTROS VOTOS ---\n")
            relatorio_conteudo.append("Nulos: (Implementar lógica para contar votos nulos)\n")
            relatorio_conteudo.append("Brancos: (Implementar lógica para contar votos brancos)\n")
            relatorio_conteudo.append("\n")

            # Salva o conteúdo no arquivo TXT no diretório atual do script
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.writelines(relatorio_conteudo)
            
            print(f"Relatório salvo em: {os.path.abspath(nome_arquivo)}")
            
            # Exibe a mensagem de sucesso usando o SnackBar
            e.page.snack_bar.content = ft.Text(f"Relatório gerado com sucesso em '{os.path.basename(nome_arquivo)}' (salvo na pasta do aplicativo).")
            e.page.snack_bar.bgcolor = "#4CAF50"  # Verde para sucesso
            e.page.snack_bar.open = True

        except sqlite3.Error as sqle:
            error_message = f"Erro no banco de dados ao gerar relatório: {sqle}"
            print(error_message) # Para depuração no console
            e.page.snack_bar.content = ft.Text(error_message)
            e.page.snack_bar.bgcolor = "#D32F2F"  # Vermelho para erro
            e.page.snack_bar.open = True
        except Exception as ex:
            general_error_message = f"Erro inesperado ao gerar relatório: {ex}"
            print(general_error_message) # Para depuração no console
            e.page.snack_bar.content = ft.Text(general_error_message)
            e.page.snack_bar.bgcolor = "#D32F2F"  # Vermelho para erro
            e.page.snack_bar.open = True
        finally:
            if conn:
                conn.close()
            e.page.update() # Garante que o SnackBar seja exibido

    def ir_grafico(e):
        e.page.go("/graficos")

    def ir_remocao(e):
        e.page.go("/admin_remocao")

    # Linha 1 de ícones
    # Linha 1 de ícones (Responsiva)
    opcoes = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=ft.GestureDetector(
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
                alignment=ft.alignment.center
            ),
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=ft.GestureDetector(
                    content=ft.Column([
                        ft.Image(src="img/admin_relatorio.png", width=150),
                        ft.Container(
                            content=ft.Text("Relatório.", size=20),
                            alignment=ft.alignment.center_right,
                            width=150
                        )
                    ], horizontal_alignment="center"),
                    on_tap=ir_relatorio
                ),
                alignment=ft.alignment.center
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80,
        run_spacing=20
    )

    # Linha 2 de ícones (Responsiva)
    opcoes2 = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=ft.GestureDetector(
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
                alignment=ft.alignment.center
            ),
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=ft.GestureDetector(
                    content=ft.Column([
                        ft.Image(src="img/admin_administrador.png", width=150),
                        ft.Container(
                            content=ft.Text("Remoção.", size=20),
                            alignment=ft.alignment.center_right,
                            width=150
                        )
                    ], horizontal_alignment="center"),
                    on_tap=ir_remocao
                ),
                alignment=ft.alignment.center
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=80,
        run_spacing=20
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
                                                ft.Container( # Centro dos ícones
                                                    content=ft.Column(
                                                        [opcoes, opcoes2],
                                                        spacing=50,
                                                        alignment="center"
                                                    ),
                                                    expand=True,
                                                    alignment=ft.alignment.center
                                                ),
                                                voltar_row # Botão no fim
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
