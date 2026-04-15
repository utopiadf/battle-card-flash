"""Battle Card Flash — App shell, state management, and routing."""
import os
import flet as ft
from typing import Callable, List, Optional

from db.repository import AbstractRepository, RepositoryFactory
from db.schema import initialize_database
from models.entities import ComparisonResult


class AppState:
    """Observable state container for the wizard flow (Observer pattern)."""

    def __init__(self):
        self._listeners: List[Callable] = []
        self.selected_product_id: Optional[int] = None
        self.selected_industry_id: Optional[int] = None
        self.selected_feature_ids: List[int] = []
        self.extra_feature_ids: List[int] = []
        self.selected_llm: str = "Qwen"
        self.comparison_result: Optional[ComparisonResult] = None
        self.is_generating: bool = False

    def add_listener(self, callback: Callable):
        self._listeners.append(callback)

    def notify(self):
        for cb in self._listeners:
            cb(self)

    def set_product(self, product_id: int):
        self.selected_product_id = product_id
        self.notify()

    def set_industry(self, industry_id: int):
        self.selected_industry_id = industry_id
        self.selected_feature_ids = []
        self.extra_feature_ids = []
        self.notify()

    def reset(self):
        self.selected_product_id = None
        self.selected_industry_id = None
        self.selected_feature_ids = []
        self.extra_feature_ids = []
        self.selected_llm = "Qwen"
        self.comparison_result = None
        self.is_generating = False


class BattleCardApp:
    """Main application controller — sets up routing and dependencies."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.state = AppState()

        # Auto-select backend: TiDB Cloud if TIDB_HOST is set, else SQLite
        if os.environ.get("TIDB_HOST"):
            self.repo: AbstractRepository = RepositoryFactory.create(
                "tidb",
                host=os.environ["TIDB_HOST"],
                port=os.environ.get("TIDB_PORT", "4000"),
                user=os.environ.get("TIDB_USER", ""),
                password=os.environ.get("TIDB_PASSWORD", ""),
                database=os.environ.get("TIDB_DB_NAME", "battlecard"),
            )
        else:
            self.db_path = "battlecard.db"
            initialize_database(self.db_path)
            self.repo = RepositoryFactory.create("sqlite", db_path=self.db_path)

    def initialize(self):
        self.page.title = "Battle Card Flash"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window.width = 900
        self.page.window.height = 700
        self.page.on_route_change = self._on_route_change
        self.page.on_view_pop = self._on_view_pop
        self.page.go("/step1")

    def _on_view_pop(self, e: ft.ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def _on_route_change(self, e: ft.RouteChangeEvent):
        self.page.views.clear()

        if self.page.route == "/step1":
            from ui.step1_select_db import build_step1_view
            self.page.views.append(build_step1_view(self.page, self.state, self.repo))
        elif self.page.route == "/step2":
            from ui.step2_select_industry import build_step2_view
            self.page.views.append(build_step2_view(self.page, self.state, self.repo))
        elif self.page.route == "/step3":
            from ui.step3_features import build_step3_view
            self.page.views.append(build_step3_view(self.page, self.state, self.repo))
        elif self.page.route == "/step4":
            from ui.step4_generate import build_step4_view
            self.page.views.append(build_step4_view(self.page, self.state, self.repo))
        else:
            from ui.step1_select_db import build_step1_view
            self.page.views.append(build_step1_view(self.page, self.state, self.repo))

        self.page.update()

