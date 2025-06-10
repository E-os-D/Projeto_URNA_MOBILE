import flet as ft
from database.db import conn, cursor
from views.home import home_view
from views.admin_login import admin_login_view
from views.eleitor_login import eleitor_login_view
from views.admin_painel import admin_painel_view
from views.cadastro_candidato import cadastro_candidato_view
from views.cadastro_admin import cadastro_admin_view
from views.votacao import votacao_view, proxima_votacao
from views.resultado import resultado_view
from views.graficos import graficos_view

def main(page: ft.Page):
    page.title = "Urna Eletrônica"
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window.maximized = True
    # page.window.width = 1920
    # page.window.height = 1200
    page.window_resizable = False

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_view())

        elif page.route == "/admin_login":
            page.views.append(admin_login_view())

        elif page.route == "/eleitor_login":
            page.views.append(eleitor_login_view())

        elif page.route == "/admin_painel":
            page.views.append(admin_painel_view())

        elif page.route == "/cadastro_candidato":
            page.views.append(cadastro_candidato_view())

        elif page.route == "/cadastro_admin":
            page.views.append(cadastro_admin_view())

        elif page.route == "/votacao_presidente":
            page.views.append(votacao_view("Presidente"))

        elif page.route == "/votacao_governador":
            page.views.append(votacao_view("Governador"))

        elif page.route == "/votacao_prefeito":
            page.views.append(votacao_view("Prefeito"))

        elif page.route == "/resultado":
            page.views.append(resultado_view())

        elif page.route == "/graficos":
            page.views.append(graficos_view())

        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)