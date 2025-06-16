import flet as ft
import sqlite3

# Importa a classe Rotate diretamente de flet
from flet import Rotate # <--- MODIFICAÇÃO PRINCIPAL

# Removidas as importações problemáticas de 'colors'.
# As cores serão agora usadas como strings literais.

# Função para estabelecer conexão com o banco de dados (reutilizada de db.py ou admin_painel.py)
def get_db_connection():
    conn = sqlite3.connect("urna_eletronica.db")
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

def graficos_view():

    # Função para buscar resultados de votação para um cargo específico
    def fetch_results(cursor, table_name, candidate_id_col, candidate_name_col, party_id_col, vote_table_name):
        query = f"""
            SELECT
                c.{candidate_name_col} AS candidato_nome,
                p.sigla AS partido_sigla,
                COUNT(v.idvotos) AS total_votos
            FROM
                {table_name} AS c
            LEFT JOIN
                {vote_table_name} AS v ON c.{candidate_id_col} = v.{candidate_id_col}
            LEFT JOIN
                Partidos AS p ON c.{party_id_col} = p.id_partido
            GROUP BY
                c.{candidate_id_col}, c.{candidate_name_col}, p.sigla
            ORDER BY
                total_votos DESC;
        """
        cursor.execute(query)
        return cursor.fetchall()

    # Função para criar um BarChart a partir dos resultados
    def create_bar_chart(title, results):
        if not results:
            return ft.Column([
                ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Nenhum dado de votação disponível para este cargo.", size=16, color="RED_500") # Usar string literal
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # Cores para os gráficos (pode expandir esta lista), agora como strings literais
        colors_list = [
            "BLUE_A700", "GREEN_A700", "RED_A700", "AMBER_700",
            "PURPLE_700", "CYAN_700", "INDIGO_700", "LIME_700"
        ]
        
        # Determine o valor máximo de votos para definir o eixo Y
        max_y = max([row['total_votos'] for row in results]) if results else 0
        interval = max(1, int(max_y / 5)) # Calcula um intervalo razoável para o eixo Y

        # Cria os BarChartRod para cada candidato
        bar_groups = []
        for i, row in enumerate(results):
            candidate_label = f"{row['candidato_nome']} ({row['partido_sigla'] or 'S/P'})"
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=row['total_votos'],
                            color=colors_list[i % len(colors_list)], # Usa a lista de strings
                            width=20,
                            border_radius=5,
                            tooltip=f"{candidate_label}: {row['total_votos']} votos"
                        )
                    ]
                )
            )

        return ft.Column(
            [
                ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.BarChart(
                        bar_groups=bar_groups,
                        border=ft.border.all(1, "GREY_400"), # Usar string literal
                        left_axis=ft.ChartAxis(
                            labels_size=40,
                            title=ft.Text("Votos", size=14, weight=ft.FontWeight.BOLD),
                            title_size=20,
                            # labels_intervals=[interval] if interval > 0 else [], # Removido 'labels_intervals'
                            show_labels=True,
                        ),
                        bottom_axis=ft.ChartAxis(
                            labels=[
                                ft.ChartAxisLabel(
                                    value=i,
                                    label=ft.Container(
                                        ft.Text(
                                            f"{row['candidato_nome'].split(' ')[0]}", # Apenas o primeiro nome para não ficar muito longo
                                            size=12,
                                            rotate=Rotate(-45 * 3.14159 / 180), # AGORA USA APENAS Rotate
                                            text_align=ft.TextAlign.RIGHT
                                        ),
                                        padding=ft.padding.only(top=5)
                                    )
                                ) for i, row in enumerate(results)
                            ],
                            labels_size=40,
                            title=ft.Text("Candidato (Partido)", size=14, weight=ft.FontWeight.BOLD),
                            title_size=20,
                            show_labels=True,
                        ),
                        horizontal_grid_lines=ft.ChartGridLines(
                            interval=interval,
                            color="GREY_300", # Usar string literal
                            width=1,
                            # enable_fade_out_for_drops=True, # REMOVIDO
                        ),
                        vertical_grid_lines=ft.ChartGridLines(
                            interval=1,
                            color="GREY_300", # Usar string literal
                            width=1,
                            # enable_fade_out_for_drops=True, # REMOVIDO
                        ),
                        # Define uma altura e largura mínimas para o gráfico, permitindo expansão
                        width=800,
                        height=400,
                        animate=ft.ChartAnimation(duration=600, ease_in_out=ft.AnimationCurve.EASE_OUT_EXPO),
                    ),
                    expand=False, # Não expandir o container do gráfico horizontalmente
                    alignment=ft.alignment.center,
                    padding=20,
                    margin=ft.margin.all(10)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30 # Espaçamento entre os gráficos
        )

    def go_back(e):
        e.page.go("/admin_painel")

    # Início da criação da View
    charts_content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obter resultados para cada cargo
        president_results = fetch_results(cursor, "Presidente", "id_número_presidente", "nome", "id_partido", "Votação_presidente")
        governor_results = fetch_results(cursor, "Governador", "id_número_governador", "nome", "id_partido", "Votação_governador")
        mayor_results = fetch_results(cursor, "Prefeito", "id_número_prefeito", "nome", "id_partido", "Votação_prefeito")

        # Adicionar os gráficos à coluna de conteúdo
        charts_content.controls.append(create_bar_chart("Votação para Presidente", president_results))
        charts_content.controls.append(create_bar_chart("Votação para Governador", governor_results))
        charts_content.controls.append(create_bar_chart("Votação para Prefeito", mayor_results))

    except sqlite3.Error as sqle:
        error_message = ft.Text(f"Erro no banco de dados ao carregar gráficos: {sqle}", color="RED_700", size=18) # Usar string literal
        charts_content.controls.append(error_message)
        print(f"Erro no banco de dados ao carregar gráficos: {sqle}")
    except Exception as ex:
        general_error_message = ft.Text(f"Erro inesperado ao carregar gráficos: {ex}", color="RED_700", size=18) # Usar string literal
        charts_content.controls.append(general_error_message)
        print(f"Erro inesperado ao carregar gráficos: {ex}")
    finally:
        if conn:
            conn.close()

    return ft.View(
        route="/graficos",
        bgcolor="#FCF8EC",
        padding=20,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=ft.Text("Gráficos de Votação", size=30, weight=ft.FontWeight.BOLD, color="BLACK"), # Usar string literal
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(bottom=20)
                        ),
                        charts_content,
                        ft.Row(
                            [ft.TextButton(
                                "← Voltar",
                                on_click=go_back,
                                style=ft.ButtonStyle(color="black") # Cor preta pode ser deixada como string literal
                            )],
                            alignment="end",
                            width=900, # Garante que o botão fique alinhado com o conteúdo
                        )
                    ]
                )
            )
        ]
    )
