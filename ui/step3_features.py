"""Step 3: Review and customize features for comparison."""
import flet as ft

from db.repository import AbstractRepository
from ui.app import AppState


def build_step3_view(page: ft.Page, state: AppState, repo: AbstractRepository) -> ft.View:
    industry = repo.get_industry(state.selected_industry_id)
    product_b = repo.get_product(state.selected_product_id)
    default_product = repo.get_default_product()
    industry_features = repo.get_features_for_industry(state.selected_industry_id)
    all_features = repo.get_all_features()

    # Track which features are selected (all industry features start checked)
    industry_feature_ids = {sf.feature.id for sf in industry_features}
    selected_ids = set(industry_feature_ids)

    # Features not already in the industry (for the "Add" dropdown)
    available_extras = [f for f in all_features if f.id not in industry_feature_ids]

    # Build checkboxes for industry features
    checkboxes = []
    for sf in industry_features:
        cb = ft.Checkbox(
            label=f"{sf.feature.name}  ({sf.feature.category})",
            value=True,
            data=sf.feature.id,
        )
        def on_check(e, fid=sf.feature.id):
            if e.control.value:
                selected_ids.add(fid)
            else:
                selected_ids.discard(fid)
        cb.on_change = on_check
        checkboxes.append(cb)

    # Container for dynamically added extra features
    extra_checkboxes = ft.Column(spacing=5)

    add_dropdown = ft.Dropdown(
        label="Add a feature",
        width=350,
        options=[ft.dropdown.Option(key=str(f.id), text=f"{f.name} ({f.category})") for f in available_extras],
        border_color=ft.Colors.BLUE_200,
    )

    def on_add_feature(e):
        if not add_dropdown.value:
            return
        fid = int(add_dropdown.value)
        feature = next((f for f in all_features if f.id == fid), None)
        if not feature or fid in selected_ids:
            return
        selected_ids.add(fid)
        state.extra_feature_ids.append(fid)
        cb = ft.Checkbox(
            label=f"{feature.name}  ({feature.category})  [added]",
            value=True,
            data=fid,
        )
        def on_extra_check(e, fid=fid):
            if e.control.value:
                selected_ids.add(fid)
            else:
                selected_ids.discard(fid)
        cb.on_change = on_extra_check
        extra_checkboxes.controls.append(cb)
        # Remove from dropdown options
        add_dropdown.options = [o for o in add_dropdown.options if o.key != str(fid)]
        add_dropdown.value = None
        page.update()

    # LLM provider selector
    from services.llm_service import LLMProviderFactory
    llm_dropdown = ft.Dropdown(
        label="AI Model",
        width=180,
        value=LLMProviderFactory.DEFAULT,
        options=[ft.dropdown.Option(n) for n in LLMProviderFactory.provider_names()],
        border_color=ft.Colors.BLUE_200,
    )

    def on_generate(e):
        state.selected_feature_ids = list(selected_ids)
        state.selected_llm = llm_dropdown.value or LLMProviderFactory.DEFAULT
        page.go("/step4")

    return ft.View(
        route="/step3",
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/step2")),
            title=ft.Text(f"Features — {industry.name}"),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        ),
        scroll=ft.ScrollMode.AUTO,
        padding=30,
        controls=[
            ft.Text(
                f"{default_product.name} vs {product_b.name} — {industry.name}",
                size=18, color=ft.Colors.BLUE_GREY_700,
            ),
            ft.Text("Select features to include in the comparison:", size=14, color=ft.Colors.GREY_600),
            ft.Container(height=10),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.BLUE_100),
                padding=ft.padding.all(15),
                content=ft.Column(spacing=5, controls=checkboxes),
            ),
            extra_checkboxes,
            ft.Container(height=15),
            ft.Row(
                controls=[
                    add_dropdown,
                    ft.ElevatedButton("Add", icon=ft.Icons.ADD, on_click=on_add_feature),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(height=20),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    llm_dropdown,
                    ft.ElevatedButton(
                    "Generate Battle Card",
                    icon=ft.Icons.AUTO_AWESOME,
                    on_click=on_generate,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=15),
                    ),
                )],
            ),
        ],
    )

