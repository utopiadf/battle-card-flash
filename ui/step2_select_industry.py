"""Step 2: Select comparison industry."""
import flet as ft

from db.repository import AbstractRepository
from ui.app import AppState

# Map icon_name strings from DB to Flet Icons
_ICON_MAP = {
    "PSYCHOLOGY": ft.Icons.PSYCHOLOGY,
    "SPORTS_ESPORTS": ft.Icons.SPORTS_ESPORTS,
    "SHOPPING_CART": ft.Icons.SHOPPING_CART,
    "ACCOUNT_BALANCE": ft.Icons.ACCOUNT_BALANCE,
    "CLOUD": ft.Icons.CLOUD,
    "STOREFRONT": ft.Icons.STOREFRONT,
}


def build_step2_view(page: ft.Page, state: AppState, repo: AbstractRepository) -> ft.View:
    industries = repo.get_all_industries()
    product_b = repo.get_product(state.selected_product_id)
    default_product = repo.get_default_product()

    def on_industry_click(industry_id: int):
        def handler(e):
            state.set_industry(industry_id)
            page.go("/step3")
        return handler

    cards = []
    for s in industries:
        icon = _ICON_MAP.get(s.icon_name, ft.Icons.CATEGORY)
        card = ft.Container(
            width=250,
            height=160,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.BLUE_100),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            ink=True,
            on_click=on_industry_click(s.id),
            padding=ft.padding.all(20),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(icon, size=40, color=ft.Colors.BLUE_700),
                    ft.Text(s.name, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        s.description[:60] + "..." if len(s.description) > 60 else s.description,
                        size=11, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )
        cards.append(card)

    return ft.View(
        route="/step2",
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/step1")),
            title=ft.Text("Select Industry"),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        ),
        padding=30,
        controls=[
            ft.Text(
                f"Comparing {default_product.name} vs {product_b.name}",
                size=18, color=ft.Colors.BLUE_GREY_700,
            ),
            ft.Text("Choose a industry for the comparison:", size=14, color=ft.Colors.GREY_600),
            ft.Container(height=10),
            ft.Row(
                wrap=True,
                spacing=20,
                run_spacing=20,
                controls=cards,
            ),
        ],
    )
