"""Step 4: Generate Battle Card Flash PPT."""
import os
import threading

import flet as ft

from db.repository import AbstractRepository
from services.comparison_service import ComparisonService
from services.llm_service import LLMService
from services.ppt_generator import PPTGenerator
from services.industry_strategy import StrategyFactory
from ui.app import AppState


def build_step4_view(page: ft.Page, state: AppState, repo: AbstractRepository) -> ft.View:
    industry = repo.get_industry(state.selected_industry_id)
    product_b = repo.get_product(state.selected_product_id)
    default_product = repo.get_default_product()

    status_text = ft.Text("Preparing comparison...", size=14, color=ft.Colors.BLUE_GREY_600)
    progress = ft.ProgressBar(width=400, color=ft.Colors.BLUE_700)
    result_container = ft.Column(visible=False, spacing=10)
    generating_container = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Icon(ft.Icons.AUTO_AWESOME, size=48, color=ft.Colors.BLUE_700),
            ft.Text("Generating Battle Card...", size=20, weight=ft.FontWeight.BOLD),
            progress,
            status_text,
        ],
    )

    def run_generation():
        try:
            # Step 1: Build comparison
            status_text.value = "Building feature comparison..."
            progress.value = 0.2
            page.update()

            cs = ComparisonService(repo)
            extra_ids = state.extra_feature_ids if state.extra_feature_ids else None
            comparison = cs.build_comparison(state.selected_product_id, state.selected_industry_id, extra_ids)

            # Step 2: Generate LLM summary
            status_text.value = "Generating AI analysis..."
            progress.value = 0.5
            page.update()

            strategy = StrategyFactory.create(industry.name)
            llm = LLMService(provider_name=state.selected_llm)
            comparison.llm_summary = llm.generate_comparison_summary(comparison, strategy)

            # Step 3: Generate PPT
            status_text.value = "Creating PPT slides..."
            progress.value = 0.8
            page.update()

            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
            os.makedirs(output_dir, exist_ok=True)
            filename = f"BattleCard_{default_product.name}_vs_{product_b.name}_{industry.name.replace(' ', '_').replace('/', '_')}.pptx"
            output_path = os.path.join(output_dir, filename)

            gen = PPTGenerator()
            gen.generate(comparison, output_path)

            # Done
            progress.value = 1.0
            status_text.value = "Complete!"
            generating_container.visible = False

            result_container.controls = [
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=64, color=ft.Colors.GREEN_600),
                ft.Text("Battle Card Generated!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                ft.Text(f"File: {filename}", size=14, color=ft.Colors.GREY_700),
                ft.Text(f"Location: {output_path}", size=12, color=ft.Colors.GREY_500, selectable=True),
                ft.Container(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        ft.ElevatedButton(
                            "Open File",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=lambda _: os.system(f'open "{output_path}"'),
                        ),
                        ft.ElevatedButton(
                            "New Comparison",
                            icon=ft.Icons.REFRESH,
                            on_click=lambda _: (state.reset(), page.go("/step1")),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
                        ),
                    ],
                ),
            ]
            result_container.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            result_container.visible = True
            page.update()

        except Exception as ex:
            generating_container.visible = False
            result_container.controls = [
                ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED_600),
                ft.Text("Generation Failed", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_800),
                ft.Text(str(ex), size=12, color=ft.Colors.RED_400, selectable=True),
                ft.ElevatedButton("Back", icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/step3")),
            ]
            result_container.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            result_container.visible = True
            page.update()

    # Start generation in background thread
    threading.Thread(target=run_generation, daemon=True).start()

    return ft.View(
        route="/step4",
        appbar=ft.AppBar(
            title=ft.Text("Generating Battle Card"),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        ),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=30,
        controls=[generating_container, result_container],
    )

