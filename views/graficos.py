import flet as ft
import sqlite3
from flet import Rotate # Keep Rotate as it's a specific control

def get_db_connection():
    conn = sqlite3.connect("urna_eletronica.db")
    conn.row_factory = sqlite3.Row
    return conn

def graficos_view():

    dropdown_ref = ft.Ref[ft.Dropdown]()
    chart_container = ft.Ref[ft.Container]() # This container will hold the chart
    
    mensagem = ft.Ref[ft.Text]() 
    
    mensagem_text_control = ft.Text(
        value="", 
        color="red500", 
        size=14, # Slightly smaller text
        weight=ft.FontWeight.BOLD,
        ref=mensagem 
    )

    def fetch_and_create_chart(cargo):
        mapping = {
            "Presidente": {
                "table": "Presidente",
                "id_col": "id_número_presidente",
                "vote_table": "Votação_presidente"
            },
            "Governador": {
                "table": "Governador",
                "id_col": "id_número_governador",
                "vote_table": "Votação_governador"
            },
            "Prefeito": {
                "table": "Prefeito",
                "id_col": "id_número_prefeito",
                "vote_table": "Votação_prefeito"
            }
        }

        data = mapping[cargo]

        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"""
            SELECT
                c.nome AS candidato_nome,
                p.sigla AS partido_sigla,
                COUNT(v.idvotos) AS total_votos
            FROM
                {data['table']} AS c
            LEFT JOIN
                {data['vote_table']} AS v ON c.{data['id_col']} = v.{data['id_col']}
            LEFT JOIN
                Partidos AS p ON c.id_partido = p.id_partido
            GROUP BY
                c.{data['id_col']}, c.nome, p.sigla
            ORDER BY
                total_votos DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        if not results:
            return ft.Text("Nenhum dado disponível.", color="red500", size=14, weight=ft.FontWeight.BOLD) # Smaller text

        # Calculate max_y for chart and ensure interval is at least 1
        max_y = max([row["total_votos"] for row in results]) if results else 0
        interval = max(1, int(max_y / 5)) if max_y > 0 else 1

        cores = [
            "blue500", "green500", "red500",
            "amber500", "purple500", "teal500",
            "cyan500", "indigo500", "orange500", "brown500" # Added more colors for variety
        ]

        bar_groups = []
        for i, row in enumerate(results):
            label = f"{row['candidato_nome']} ({row['partido_sigla'] or 'S/P'})"
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=row['total_votos'],
                            color=cores[i % len(cores)],
                            width=20, # Slightly narrower bars
                            border_radius=5,
                            tooltip=f"{label}: {row['total_votos']} votos"
                        )
                    ]
                )
            )

        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, "grey300"),
            left_axis=ft.ChartAxis(
                labels_size=25, # Smaller labels
                show_labels=True,
                title=ft.Text("Votos", size=12, weight=ft.FontWeight.BOLD, color="black") # Smaller title
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(
                            ft.Text(
                                # Use the first name for brevity on chart labels, or full name if short
                                row['candidato_nome'].split()[0] if len(row['candidato_nome'].split()[0]) < 10 else row['candidato_nome'], 
                                size=10, # Smaller text for labels
                                rotate=Rotate(-45 * 3.14159 / 180), 
                                text_align=ft.TextAlign.RIGHT,
                                color="black"
                            ),
                            padding=ft.padding.only(top=3) # Reduced padding
                        )
                    )
                    for i, row in enumerate(results)
                ],
                labels_size=25, # Smaller labels
                show_labels=True,
                title=ft.Text("Candidato", size=12, weight=ft.FontWeight.BOLD, color="black") # Smaller title
            ),
            horizontal_grid_lines=ft.ChartGridLines(interval=interval, color="grey300", width=0.8),
            vertical_grid_lines=ft.ChartGridLines(interval=1, color="grey300", width=0.8),
            width=max(400, len(results) * 40), # Reduced minimum width, adjusted multiplier
            height=300, # Reduced height
            expand=True # Allow the chart to expand within its container
        )

        return ft.Container(
            content=chart,
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=5, right=10, top=10, bottom=5) # Reduced padding
        )

    def ver_grafico(e):
        cargo = dropdown_ref.current.value
        if not cargo:
            mensagem.current.value = "Por favor, selecione um cargo." 
            mensagem.current.color = "red500" 
            chart_container.current.content = None
        else:
            mensagem.current.value = "" 
            chart = fetch_and_create_chart(cargo)
            chart_container.current.content = chart
        e.page.update()

    def go_back(e):
        e.page.go("/admin_painel")

    return ft.View(
        route="/graficos_por_cargo",
        bgcolor="#D6CEE5",
        padding=20, # Changed from 100 to 20
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
                                        col={"xs": 12, "sm": 7, "md": 8, "lg": 6, "xl": 4}, # Adjusted column sizes
                                        padding=40, # Changed from 20 to 40
                                        bgcolor="white",
                                        border=ft.border.all(width=1, color="black"),
                                        shadow=ft.BoxShadow(
                                            spread_radius=0,
                                            blur_radius=0,
                                            color="black",
                                            offset=ft.Offset(15, 15) # Changed from 10, 10 to 15, 15
                                        ),
                                        content=ft.Column(
                                            scroll=ft.ScrollMode.AUTO, 
                                            alignment=ft.MainAxisAlignment.START, 
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    content=ft.Text("Visualizar Gráfico de Votação", size=32, weight="bold"), # Changed from 24 to 32
                                                    padding=ft.padding.only(bottom=50) # Changed from 30 to 50
                                                ),
                                                ft.ResponsiveRow( # Use ResponsiveRow here for the dropdown and button
                                                    alignment=ft.MainAxisAlignment.CENTER, 
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                                                    controls=[
                                                        ft.Container(
                                                            col={"xs": 12, "sm": 7, "md": 7, "lg": 8}, # Full width on extra small, smaller on others
                                                            content=ft.Dropdown(
                                                                ref=dropdown_ref,
                                                                label="Selecione o cargo", 
                                                                options=[
                                                                    ft.dropdown.Option("Presidente"),
                                                                    ft.dropdown.Option("Governador"),
                                                                    ft.dropdown.Option("Prefeito")
                                                                ],
                                                                expand=True, # Allow dropdown to expand within its column
                                                                bgcolor="#D6CEE5", 
                                                                color="#000000", 
                                                                label_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500), 
                                                                border_radius=ft.border_radius.all(40), 
                                                                content_padding=ft.Padding(top=18, bottom=18, left=14, right=14) 
                                                            ),
                                                        ),
                                                        ft.Container( # The "VER GRÁFICO" button container
                                                            col={"xs": 12, "sm": 5, "md": 5, "lg": 4}, # Full width on extra small, smaller on others
                                                            content=ft.Container(
                                                                content=ft.Text("VER GRÁFICO", size=16, weight="bold", color="black"), # Changed from 14 to 16
                                                                alignment=ft.alignment.center,
                                                                height=50, # Changed from 40 to 50
                                                                bgcolor="#FCF8EC",
                                                                border=ft.border.all(1, "black"),
                                                                margin=ft.margin.only(top=5, left=5), # Changed from top=3, left=3 to top=5, left=5
                                                                ink=True,
                                                                on_click=ver_grafico,
                                                                shadow=ft.BoxShadow(
                                                                    spread_radius=0,
                                                                    blur_radius=0,
                                                                    color="black",
                                                                    offset=ft.Offset(5, 5) # Changed from 3, 3 to 5, 5
                                                                )
                                                            ),
                                                            alignment=ft.alignment.center # Center the button within its column
                                                        ),
                                                    ]
                                                ),
                                                ft.Container(height=20), # Changed from 15 to 20
                                                mensagem_text_control, 
                                                ft.Container(height=20), # Changed from 15 to 20
                                                ft.Container(
                                                    ref=chart_container,
                                                    expand=True,
                                                    alignment=ft.alignment.center,
                                                    padding=ft.padding.only(top=15)
                                                ),
                                                ft.Container(height=20), # Changed from 15 to 20
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.END,
                                                    controls=[
                                                        ft.TextButton(
                                                            "← Voltar",
                                                            on_click=go_back,
                                                            style=ft.ButtonStyle(color="black") 
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
            )
        ]
    )