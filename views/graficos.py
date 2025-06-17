






# import flet as ft
# import sqlite3
# from flet import Rotate # Keep Rotate as it's a specific control

# def get_db_connection():
#     conn = sqlite3.connect("urna_eletronica.db")
#     conn.row_factory = sqlite3.Row
#     return conn

# def graficos_selecao_view():

#     dropdown_ref = ft.Ref[ft.Dropdown]()
#     chart_container = ft.Ref[ft.Container]() # This container will hold the chart
#     mensagem = ft.Ref[ft.Text]()

#     # Função para buscar dados e montar o gráfico
#     def fetch_and_create_chart(cargo):
#         mapping = {
#             "Presidente": {
#                 "table": "Presidente",
#                 "id_col": "id_número_presidente",
#                 "vote_table": "Votação_presidente"
#             },
#             "Governador": {
#                 "table": "Governador",
#                 "id_col": "id_número_governador",
#                 "vote_table": "Votação_governador"
#             },
#             "Prefeito": {
#                 "table": "Prefeito",
#                 "id_col": "id_número_prefeito",
#                 "vote_table": "Votação_prefeito"
#             }
#         }

#         data = mapping[cargo]

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = f"""
#             SELECT
#                 c.nome AS candidato_nome,
#                 p.sigla AS partido_sigla,
#                 COUNT(v.idvotos) AS total_votos
#             FROM
#                 {data['table']} AS c
#             LEFT JOIN
#                 {data['vote_table']} AS v ON c.{data['id_col']} = v.{data['id_col']}
#             LEFT JOIN
#                 Partidos AS p ON c.id_partido = p.id_partido
#             GROUP BY
#                 c.{data['id_col']}, c.nome, p.sigla
#             ORDER BY
#                 total_votos DESC;
#         """
#         cursor.execute(query)
#         results = cursor.fetchall()
#         conn.close()

#         if not results:
#             return ft.Text("Nenhum dado disponível.", color="red500", size=16, weight=ft.FontWeight.BOLD)

#         max_y = max([row["total_votos"] for row in results])
#         interval = max(1, int(max_y / 5))

#         cores = [
#             "blue500", "green500", "red500",
#             "amber500", "purple500", "teal500",
#             "cyan500", "indigo500"
#         ]

#         bar_groups = []
#         for i, row in enumerate(results):
#             label = f"{row['candidato_nome']} ({row['partido_sigla'] or 'S/P'})"
#             bar_groups.append(
#                 ft.BarChartGroup(
#                     x=i,
#                     bar_rods=[
#                         ft.BarChartRod(
#                             from_y=0,
#                             to_y=row['total_votos'],
#                             color=cores[i % len(cores)],
#                             width=25, # Slightly wider bars
#                             border_radius=5,
#                             tooltip=f"{label}: {row['total_votos']} votos"
#                         )
#                     ]
#                 )
#             )

#         chart = ft.BarChart(
#             bar_groups=bar_groups,
#             border=ft.border.all(1, "grey300"),
#             left_axis=ft.ChartAxis(
#                 labels_size=30,
#                 show_labels=True,
#                 title=ft.Text("Votos", size=14, weight=ft.FontWeight.BOLD, color="black")
#             ),
#             bottom_axis=ft.ChartAxis(
#                 labels=[
#                     ft.ChartAxisLabel(
#                         value=i,
#                         label=ft.Container(
#                             ft.Text(
#                                 row['candidato_nome'].split()[0], # Show only first name
#                                 size=12,
#                                 rotate=Rotate(-45 * 3.14159 / 180), # Rotate labels for better fit
#                                 text_align=ft.TextAlign.RIGHT,
#                                 color="black"
#                             ),
#                             padding=ft.padding.only(top=5)
#                         )
#                     )
#                     for i, row in enumerate(results)
#                 ],
#                 labels_size=30,
#                 show_labels=True,
#                 title=ft.Text("Candidato", size=14, weight=ft.FontWeight.BOLD, color="black")
#             ),
#             horizontal_grid_lines=ft.ChartGridLines(interval=interval, color="grey300", width=0.8),
#             vertical_grid_lines=ft.ChartGridLines(interval=1, color="grey300", width=0.8),
#             width=650,
#             height=400,
#             # REMOVED: padding=ft.padding.only(left=10, right=20, top=20, bottom=10)
#         )

#         # Wrap the chart in a container for specific chart padding if desired,
#         # otherwise, the padding of chart_container will apply.
#         return ft.Container(
#             content=chart,
#             padding=ft.padding.only(left=10, right=20, top=20, bottom=10) # Apply padding here
#         )


#     def ver_grafico(e):
#         cargo = dropdown_ref.current.value
#         if not cargo:
#             mensagem.current.value = "Por favor, selecione um cargo."
#             mensagem.current.color = "red500"
#             chart_container.current.content = None
#         else:
#             mensagem.current.value = ""
#             chart = fetch_and_create_chart(cargo)
#             chart_container.current.content = chart
#         e.page.update()

#     def go_back(e):
#         e.page.go("/admin_painel")

#     return ft.View(
#         route="/graficos_por_cargo",
#         bgcolor="grey100",
#         padding=30,
#         controls=[
#             ft.Container(
#                 width=800,
#                 padding=30,
#                 bgcolor="white",
#                 border_radius=ft.border_radius.all(10),
#                 shadow=ft.BoxShadow(
#                     blur_radius=15,
#                     color="black26",
#                     offset=ft.Offset(0, 5)
#                 ),
#                 content=ft.Column(
#                     [
#                         ft.Text(
#                             "Visualizar Gráfico de Votação",
#                             size=28,
#                             weight=ft.FontWeight.BOLD,
#                             color="bluegrey900"
#                         ),
#                         ft.Divider(height=20, color="transparent"),
#                         ft.Row(
#                             [
#                                 ft.Dropdown(
#                                     ref=dropdown_ref,
#                                     label="Selecione o cargo",
#                                     options=[
#                                         ft.dropdown.Option("Presidente"),
#                                         ft.dropdown.Option("Governador"),
#                                         ft.dropdown.Option("Prefeito")
#                                     ],
#                                     width=250,
#                                     border_radius=5,
#                                     filled=True,
#                                     bgcolor="white"
#                                 ),
#                                 ft.ElevatedButton(
#                                     "Ver gráfico",
#                                     on_click=ver_grafico,
#                                     bgcolor="blue700",
#                                     color="white",
#                                     style=ft.ButtonStyle(
#                                         shape=ft.RoundedRectangleBorder(radius=5),
#                                         padding=ft.padding.symmetric(horizontal=20, vertical=10)
#                                     ),
#                                     elevation=3
#                                 ),
#                             ],
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             spacing=20
#                         ),
#                         ft.Text(
#                             "",
#                             color="red500",
#                             ref=mensagem,
#                             size=14,
#                             weight=ft.FontWeight.BOLD
#                         ),
#                         ft.Container(
#                             ref=chart_container,
#                             alignment=ft.alignment.center,
#                             # The padding here will affect the spacing around the chart
#                             # if the chart itself doesn't have internal padding.
#                             padding=ft.padding.only(top=20)
#                         ),
#                         ft.Divider(height=20, color="transparent"),
#                         ft.TextButton(
#                             "← Voltar",
#                             on_click=go_back,
#                             style=ft.ButtonStyle(color="blue700")
#                         )
#                     ],
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     spacing=15
#                 )
#             )
#         ],
#         vertical_alignment=ft.CrossAxisAlignment.CENTER,
#         horizontal_alignment=ft.CrossAxisAlignment.CENTER
#     )

# ______________________________________________________________________________________________

# Com biblioteca

# import flet as ft
# import sqlite3
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

# def get_db_connection():
#     conn = sqlite3.connect("urna_eletronica.db")
#     conn.row_factory = sqlite3.Row
#     return conn

# def graficos_selecao_view():

#     dropdown_ref = ft.Ref[ft.Dropdown]()
#     chart_container = ft.Ref[ft.Container]()
#     mensagem = ft.Ref[ft.Text]()

#     def fetch_and_create_chart(cargo):
#         mapping = {
#             "Presidente": {
#                 "table": "Presidente",
#                 "id_col": "id_número_presidente",
#                 "vote_table": "Votação_presidente"
#             },
#             "Governador": {
#                 "table": "Governador",
#                 "id_col": "id_número_governador",
#                 "vote_table": "Votação_governador"
#             },
#             "Prefeito": {
#                 "table": "Prefeito",
#                 "id_col": "id_número_prefeito",
#                 "vote_table": "Votação_prefeito"
#             }
#         }

#         data = mapping[cargo]

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = f"""
#             SELECT
#                 c.nome AS candidato_nome,
#                 p.sigla AS partido_sigla,
#                 COUNT(v.idvotos) AS total_votos
#             FROM
#                 {data['table']} AS c
#             LEFT JOIN
#                 {data['vote_table']} AS v ON c.{data['id_col']} = v.{data['id_col']}
#             LEFT JOIN
#                 Partidos AS p ON c.id_partido = p.id_partido
#             GROUP BY
#                 c.{data['id_col']}, c.nome, p.sigla
#             ORDER BY
#                 total_votos DESC;
#         """
#         cursor.execute(query)
#         results = cursor.fetchall()
#         conn.close()

#         if not results:
#             return ft.Text("Nenhum dado disponível.", color="RED")

#         # Dados para o gráfico
#         labels = [f"{row['candidato_nome'].split()[0]} ({row['partido_sigla'] or 'S/P'})" for row in results]
#         sizes = [row['total_votos'] for row in results]
#         colors = plt.cm.Pastel1.colors

#         # Criar gráfico com matplotlib
#         fig, ax = plt.subplots()
#         ax.pie(sizes, labels=labels, colors=colors[:len(labels)], startangle=90, autopct='%1.1f%%')
#         ax.axis('equal')  # Deixa o círculo perfeito
#         fig.set_facecolor("white")

#         # Salvar imagem em base64
#         buf = BytesIO()
#         plt.savefig(buf, format="png", bbox_inches='tight')
#         plt.close(fig)
#         buf.seek(0)
#         img_base64 = base64.b64encode(buf.read()).decode("utf-8")

#         return ft.Image(src_base64=img_base64, width=500, height=500)

#     def ver_grafico(e):
#         cargo = dropdown_ref.current.value
#         if not cargo:
#             mensagem.current.value = "Por favor, selecione um cargo."
#             chart_container.current.content = None
#         else:
#             mensagem.current.value = ""
#             chart = fetch_and_create_chart(cargo)
#             chart_container.current.content = chart
#         e.page.update()

#     def go_back(e):
#         e.page.go("/admin_painel")

#     return ft.View(
#         route="/graficos_por_cargo",
#         bgcolor="#F5F5F5",
#         padding=30,
#         controls=[
#             ft.Column([
#                 ft.Text("Gráfico de Votos", size=28, weight=ft.FontWeight.BOLD),
#                 ft.Dropdown(
#                     ref=dropdown_ref,
#                     label="Selecione o cargo",
#                     options=[
#                         ft.dropdown.Option("Presidente"),
#                         ft.dropdown.Option("Governador"),
#                         ft.dropdown.Option("Prefeito")
#                     ],
#                     width=300
#                 ),
#                 ft.ElevatedButton("Ver gráfico", on_click=ver_grafico),
#                 ft.Text("", color="RED", ref=mensagem),
#                 ft.Container(padding=20, ref=chart_container),
#                 ft.Row(
#                     [ft.TextButton("→ Voltar.", on_click=go_back)],
#                     alignment=ft.MainAxisAlignment.END
#                 )
#             ],
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER)
#         ]
#     )
