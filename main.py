import flet as ft
from ui.app import BattleCardApp


def main(page: ft.Page):
    app = BattleCardApp(page)
    app.initialize()


ft.app(target=main)