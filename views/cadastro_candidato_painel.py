import flet as ft

def cadastro_candidato_painel_view():
    def cargo_botao(nome, rota):
        return ft.Container(
            content=ft.Text(nome, size=16, weight="bold", color="black"),
            alignment=ft.alignment.center,
            width=220,
            height=50,
            bgcolor="#FCF8EC",
            border=ft.border.all(1, "black"),
            margin=ft.margin.only(top=5, left=5),
            ink=True,
            on_click=lambda e: e.page.go(rota),
            on_hover=lambda e: on_hover(e),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=0,
                color="black",
                offset=ft.Offset(5, 5)
            )
        )

    def on_hover(e):
        txt = e.control.content
        if isinstance(txt, ft.Text):
            if e.data == "true":
                e.control.bgcolor = "#F2EEE3" 
                e.control.border = ft.border.all(1, "black")
                txt.color = "black"
            else:
                e.control.bgcolor = "#FCF8EC"
                e.control.border = ft.border.all(1, "black")
                txt.color = "black"
            e.control.update()

    return ft.View(
        route="/cadastro_candidato_painel",
        bgcolor="#DFEDFF",
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
                                scroll=ft.ScrollMode.AUTO,
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
                                    cargo_botao("Presidente", "/cadastro_candidato"),
                                    cargo_botao("Governador", "/cadastro_governador"),
                                    cargo_botao("Prefeito", "/cadastro_prefeito"),
                                    cargo_botao("Partido", "/cadastro_partido"),
                                    cargo_botao("Administrador", "/cadastro_admin"),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        controls=[
                                            ft.TextButton(
                                                "← Voltar.",
                                                style=ft.ButtonStyle(color="black"),
                                                on_click=lambda e: e.page.go("/admin_painel")
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
