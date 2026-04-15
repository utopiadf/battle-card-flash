"""Step 1: Select target database to compare against TiDB."""
import flet as ft

from db.repository import AbstractRepository
from ui.app import AppState


def build_step1_view(page: ft.Page, state: AppState, repo: AbstractRepository) -> ft.View:
    products = repo.get_all_products()
    default_product = repo.get_default_product()
    other_products = [p for p in products if not p.is_default]

    dropdown = ft.Dropdown(
        label="Select a database to compare",
        width=400,
        options=[ft.dropdown.Option(key=str(p.id), text=p.name) for p in other_products],
        border_color=ft.Colors.BLUE_200,
    )

    error_text = ft.Text("", color=ft.Colors.RED_400, size=12)

    def on_next(e):
        if not dropdown.value:
            error_text.value = "Please select a database first."
            page.update()
            return
        state.set_product(int(dropdown.value))
        page.go("/step2")

    return ft.View(
        route="/step1",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.BLUE_50, ft.Colors.WHITE],
                ),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.COMPARE_ARROWS, size=64, color=ft.Colors.BLUE_700),
                        ft.Text("Battle Card Flash", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Text(
                            f"Compare {default_product.name} with another database",
                            size=16, color=ft.Colors.BLUE_GREY_600,
                        ),
                        ft.Container(height=20),
                        dropdown,
                        error_text,
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Next: Select Industry",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=on_next,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                text_style=ft.TextStyle(size=20),
                                padding=ft.padding.symmetric(horizontal=60, vertical=30),
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
