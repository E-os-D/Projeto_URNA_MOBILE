import flet as ft

def cadastro_candidato_painel_view():
    def cargo_botao(nome, rota):
        txt = ft.Text(nome, size=16, weight=ft.FontWeight.BOLD, color="black")

        def on_hover(e):
            if e.data == "true":
                e.control.content.controls[1].bgcolor = "black"
                txt.color = "white"
            else:
                e.control.content.controls[1].bgcolor = "#FAF7F1"
                txt.color = "black"
            e.control.update()

        return ft.Container(
            width=220,
            height=50,
            on_click=lambda e: e.page.go(rota),
            on_hover=on_hover,
            content=ft.Stack(
                controls=[
                    # Quadrado preto ao fundo
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="black",
                        left=3,
                        top=3,
                        border_radius=ft.border_radius.all(0),  # sem bordas arredondadas
                    ),
                    # Botão principal
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="#FAF7F1",
                        border=ft.border.all(1, "black"),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(0),
                        content=txt,
                        ink=True,
                    )
                ]
            )
        )

        return ft.Container(
            width=220,
            height=50,
            on_click=lambda e: e.page.go(rota),
            on_hover=on_hover,
            content=ft.Stack(
                controls=[
                    # Quadrado preto ao fundo (simulando sombra sólida)
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="black",
                        left=4,
                        top=4,
                        border_radius=ft.border_radius.all(2),
                    ),
                    # Botão principal
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="#FAF7F1",
                        border=ft.border.all(1, "black"),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(2),
                        content=txt,
                        ink=True,
                    ),
                ]
            )
        )



        return ft.Container(
            width=220,
            height=50,
            on_click=lambda e: e.page.go(rota),
            on_hover=on_hover,
            content=ft.Stack(
                controls=[
                    # Sombra
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="black",
                        left=3,
                        top=3,
                        border_radius=ft.border_radius.all(2),
                    ),
                    # Botão principal
                    ft.Container(
                        width=220,
                        height=50,
                        bgcolor="#FAF7F1",
                        border=ft.border.all(1, "black"),
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(2),
                        content=txt,
                        ink=True,
                    )
                ]
            )
        )

    return ft.View(
        route="/cadastro_candidato_painel",
        bgcolor="#DFEDFF",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
                content=ft.Container(
                    width=500,
                    height=420,
                    bgcolor="white",
                    border=ft.border.all(1, "black"),
                    padding=40,
                    content=ft.Column(
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Quem deseja cadastrar?",
                                size=24,
                                weight=ft.FontWeight.W_600,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            cargo_botao("Presidente", "/cadastro_presidente"),
                            cargo_botao("Governador", "/cadastro_governador"),
                            cargo_botao("Prefeito", "/cadastro_prefeito"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    # Botão voltar simples (sem sombra)
                                    ft.TextButton(
                                        "→ Voltar.",
                                        style=ft.ButtonStyle(color="black"),
                                        on_click=lambda e: e.page.go("/admin_painel")
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        ]
    )
