import flet as ft

def remocao_painel_view(page: ft.Page):
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
        route="/remocao_painel",
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
                                        "Quem deseja remover?",  
                                        size=24,
                                        weight=ft.FontWeight.W_600,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(
                                        content=ft.ResponsiveRow(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=page.window_width > 800 and 30 or 10,  # maior espaçamento em telas largas
                                            run_spacing=page.window_width > 800 and 30 or 10,
                                            controls=[
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Presidente", "/")),
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Governador", "/")),
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Prefeito", "/")),
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Partido", "/")),
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Administrador", "/")),
                                                ft.Container(col={"xs": 12, "sm": 6}, content=cargo_botao("Eleitor", "/")),
                                            ]
                                        )
                                    ),
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
