"""Repository pattern for database access."""
import json
import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from models.entities import (
    CaseStudy,
    ExpertAdvice,
    Feature,
    Product,
    IndustryFeature,
    Industry,
)


class AbstractRepository(ABC):
    """Abstract interface for data access."""

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        ...

    @abstractmethod
    def get_default_product(self) -> Product:
        ...

    @abstractmethod
    def get_product(self, product_id: int) -> Optional[Product]:
        ...

    @abstractmethod
    def get_all_industries(self) -> List[Industry]:
        ...

    @abstractmethod
    def get_industry(self, industry_id: int) -> Optional[Industry]:
        ...

    @abstractmethod
    def get_features_for_industry(self, industry_id: int) -> List[IndustryFeature]:
        ...

    @abstractmethod
    def get_all_features(self) -> List[Feature]:
        ...

    @abstractmethod
    def get_product_feature_values(
        self, product_id: int, feature_ids: List[int]
    ) -> Dict[int, str]:
        ...

    @abstractmethod
    def get_expert_advice(
        self, industry_id: int, product_a_id: int, product_b_id: int
    ) -> List[ExpertAdvice]:
        ...

    @abstractmethod
    def get_case_studies(
        self, industry_id: int, product_id: int
    ) -> List[CaseStudy]:
        ...

    @abstractmethod
    def add_feature_to_industry(
        self, industry_id: int, feature_id: int, weight: float = 0.5
    ) -> None:
        ...

    @abstractmethod
    def save_comparison_history(
        self,
        product_a_id: int,
        product_b_id: int,
        industry_id: int,
        feature_ids: List[int],
        ppt_path: str,
        llm_summary: str,
    ) -> int:
        ...


class SQLiteRepository(AbstractRepository):
    """SQLite implementation of the repository."""

    def __init__(self, db_path: str = "battlecard.db"):
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        self._conn.close()

    # -- Products --

    def get_all_products(self) -> List[Product]:
        rows = self._conn.execute(
            "SELECT * FROM products ORDER BY is_default DESC, name"
        ).fetchall()
        return [self._row_to_product(r) for r in rows]

    def get_default_product(self) -> Product:
        row = self._conn.execute(
            "SELECT * FROM products WHERE is_default = 1"
        ).fetchone()
        return self._row_to_product(row)

    def get_product(self, product_id: int) -> Optional[Product]:
        row = self._conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        return self._row_to_product(row) if row else None

    # -- Industries --

    def get_all_industries(self) -> List[Industry]:
        rows = self._conn.execute(
            "SELECT * FROM industries ORDER BY sort_order, name"
        ).fetchall()
        return [self._row_to_industry(r) for r in rows]

    def get_industry(self, industry_id: int) -> Optional[Industry]:
        row = self._conn.execute(
            "SELECT * FROM industries WHERE id = ?", (industry_id,)
        ).fetchone()
        return self._row_to_industry(row) if row else None

    # -- Features --

    def get_all_features(self) -> List[Feature]:
        rows = self._conn.execute(
            "SELECT * FROM features ORDER BY category, name"
        ).fetchall()
        return [self._row_to_feature(r) for r in rows]

    def get_features_for_industry(self, industry_id: int) -> List[IndustryFeature]:
        rows = self._conn.execute(
            """SELECT f.*, sf.weight, sf.sort_order AS sf_sort
               FROM features f
               JOIN industry_features sf ON sf.feature_id = f.id
               WHERE sf.industry_id = ?
               ORDER BY sf.sort_order, f.category, f.name""",
            (industry_id,),
        ).fetchall()
        return [
            IndustryFeature(
                feature=self._row_to_feature(r),
                weight=r["weight"],
                sort_order=r["sf_sort"],
            )
            for r in rows
        ]

    def get_product_feature_values(
        self, product_id: int, feature_ids: List[int]
    ) -> Dict[int, str]:
        if not feature_ids:
            return {}
        placeholders = ",".join("?" for _ in feature_ids)
        rows = self._conn.execute(
            f"SELECT feature_id, value FROM product_features "
            f"WHERE product_id = ? AND feature_id IN ({placeholders})",
            [product_id] + feature_ids,
        ).fetchall()
        return {r["feature_id"]: r["value"] for r in rows}

    # -- Expert Advice --

    def get_expert_advice(
        self, industry_id: int, product_a_id: int, product_b_id: int
    ) -> List[ExpertAdvice]:
        rows = self._conn.execute(
            """SELECT * FROM expert_advice
               WHERE industry_id = ?
                 AND product_a_id = ? AND product_b_id = ?
               ORDER BY created_at""",
            (industry_id, product_a_id, product_b_id),
        ).fetchall()
        return [
            ExpertAdvice(
                id=r["id"],
                industry_id=r["industry_id"],
                product_a_id=r["product_a_id"],
                product_b_id=r["product_b_id"],
                advice_text=r["advice_text"],
                author=r["author"] or "",
            )
            for r in rows
        ]

    def get_case_studies(
        self, industry_id: int, product_id: int
    ) -> List[CaseStudy]:
        rows = self._conn.execute(
            """SELECT * FROM case_studies
               WHERE industry_id = ? AND product_id = ?
               ORDER BY created_at""",
            (industry_id, product_id),
        ).fetchall()
        return [
            CaseStudy(
                id=r["id"],
                industry_id=r["industry_id"],
                product_id=r["product_id"],
                title=r["title"],
                customer=r["customer"],
                summary=r["summary"],
                results=r["results"] or "",
                source_url=r["source_url"] or "",
            )
            for r in rows
        ]

    # -- Mutations --

    def add_feature_to_industry(
        self, industry_id: int, feature_id: int, weight: float = 0.5
    ) -> None:
        self._conn.execute(
            """INSERT OR IGNORE INTO industry_features (industry_id, feature_id, weight)
               VALUES (?, ?, ?)""",
            (industry_id, feature_id, weight),
        )
        self._conn.commit()

    def save_comparison_history(
        self,
        product_a_id: int,
        product_b_id: int,
        industry_id: int,
        feature_ids: List[int],
        ppt_path: str,
        llm_summary: str,
    ) -> int:
        cursor = self._conn.execute(
            """INSERT INTO comparison_history
               (product_a_id, product_b_id, industry_id, feature_ids, ppt_path, llm_summary)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (product_a_id, product_b_id, industry_id, json.dumps(feature_ids), ppt_path, llm_summary),
        )
        self._conn.commit()
        return cursor.lastrowid

    # -- Row mappers --

    @staticmethod
    def _row_to_product(row: sqlite3.Row) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            vendor=row["vendor"],
            description=row["description"] or "",
            logo_path=row["logo_path"] or "",
            website_url=row["website_url"] or "",
            is_default=bool(row["is_default"]),
        )

    @staticmethod
    def _row_to_industry(row: sqlite3.Row) -> Industry:
        return Industry(
            id=row["id"],
            name=row["name"],
            description=row["description"] or "",
            icon_name=row["icon_name"],
            sort_order=row["sort_order"],
        )

    @staticmethod
    def _row_to_feature(row: sqlite3.Row) -> Feature:
        return Feature(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            description=row["description"] or "",
            data_type=row["data_type"],
        )


class TiDBCloudRepository(AbstractRepository):
    """TiDB Cloud Serverless implementation of the repository."""

    def __init__(self, **kwargs):
        import pymysql
        import ssl
        from db.schema import initialize_tidb_database

        ssl_ctx = ssl.create_default_context()
        self._conn = pymysql.connect(
            host=kwargs.get("host", ""),
            port=int(kwargs.get("port", 4000)),
            user=kwargs.get("user", ""),
            password=kwargs.get("password", ""),
            database=kwargs.get("database", ""),
            ssl=ssl_ctx,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
        initialize_tidb_database(self._conn)

    def close(self):
        self._conn.close()

    def _query(self, sql, params=None):
        cursor = self._conn.cursor()
        cursor.execute(sql, params or ())
        return cursor.fetchall()

    def _query_one(self, sql, params=None):
        cursor = self._conn.cursor()
        cursor.execute(sql, params or ())
        return cursor.fetchone()

    def _execute(self, sql, params=None):
        cursor = self._conn.cursor()
        cursor.execute(sql, params or ())
        self._conn.commit()
        return cursor

    # -- Products --

    def get_all_products(self) -> List[Product]:
        rows = self._query("SELECT * FROM products ORDER BY is_default DESC, name")
        return [self._row_to_product(r) for r in rows]

    def get_default_product(self) -> Product:
        return self._row_to_product(
            self._query_one("SELECT * FROM products WHERE is_default = 1")
        )

    def get_product(self, product_id: int) -> Optional[Product]:
        row = self._query_one("SELECT * FROM products WHERE id = %s", (product_id,))
        return self._row_to_product(row) if row else None

    # -- Industries --

    def get_all_industries(self) -> List[Industry]:
        rows = self._query("SELECT * FROM industries ORDER BY sort_order, name")
        return [self._row_to_industry(r) for r in rows]

    def get_industry(self, industry_id: int) -> Optional[Industry]:
        row = self._query_one("SELECT * FROM industries WHERE id = %s", (industry_id,))
        return self._row_to_industry(row) if row else None

    # -- Features --

    def get_all_features(self) -> List[Feature]:
        rows = self._query("SELECT * FROM features ORDER BY category, name")
        return [self._row_to_feature(r) for r in rows]

    def get_features_for_industry(self, industry_id: int) -> List[IndustryFeature]:
        rows = self._query(
            """SELECT f.*, sf.weight, sf.sort_order AS sf_sort
               FROM features f
               JOIN industry_features sf ON sf.feature_id = f.id
               WHERE sf.industry_id = %s
               ORDER BY sf.sort_order, f.category, f.name""",
            (industry_id,),
        )
        return [
            IndustryFeature(
                feature=self._row_to_feature(r),
                weight=r["weight"],
                sort_order=r["sf_sort"],
            )
            for r in rows
        ]

    def get_product_feature_values(
        self, product_id: int, feature_ids: List[int]
    ) -> Dict[int, str]:
        if not feature_ids:
            return {}
        placeholders = ",".join("%s" for _ in feature_ids)
        rows = self._query(
            f"SELECT feature_id, value FROM product_features "
            f"WHERE product_id = %s AND feature_id IN ({placeholders})",
            [product_id] + feature_ids,
        )
        return {r["feature_id"]: r["value"] for r in rows}

    # -- Expert Advice --

    def get_expert_advice(
        self, industry_id: int, product_a_id: int, product_b_id: int
    ) -> List[ExpertAdvice]:
        rows = self._query(
            """SELECT * FROM expert_advice
               WHERE industry_id = %s AND product_a_id = %s AND product_b_id = %s
               ORDER BY created_at""",
            (industry_id, product_a_id, product_b_id),
        )
        return [
            ExpertAdvice(
                id=r["id"], industry_id=r["industry_id"],
                product_a_id=r["product_a_id"], product_b_id=r["product_b_id"],
                advice_text=r["advice_text"], author=r["author"] or "",
            )
            for r in rows
        ]

    def get_case_studies(self, industry_id: int, product_id: int) -> List[CaseStudy]:
        rows = self._query(
            """SELECT * FROM case_studies
               WHERE industry_id = %s AND product_id = %s
               ORDER BY created_at""",
            (industry_id, product_id),
        )
        return [
            CaseStudy(
                id=r["id"], industry_id=r["industry_id"], product_id=r["product_id"],
                title=r["title"], customer=r["customer"], summary=r["summary"],
                results=r["results"] or "", source_url=r["source_url"] or "",
            )
            for r in rows
        ]

    # -- Mutations --

    def add_feature_to_industry(
        self, industry_id: int, feature_id: int, weight: float = 0.5
    ) -> None:
        self._execute(
            """INSERT IGNORE INTO industry_features (industry_id, feature_id, weight)
               VALUES (%s, %s, %s)""",
            (industry_id, feature_id, weight),
        )

    def save_comparison_history(
        self, product_a_id: int, product_b_id: int, industry_id: int,
        feature_ids: List[int], ppt_path: str, llm_summary: str,
    ) -> int:
        cursor = self._execute(
            """INSERT INTO comparison_history
               (product_a_id, product_b_id, industry_id, feature_ids, ppt_path, llm_summary)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (product_a_id, product_b_id, industry_id, json.dumps(feature_ids), ppt_path, llm_summary),
        )
        return cursor.lastrowid

    # -- Row mappers --

    @staticmethod
    def _row_to_product(row) -> Product:
        return Product(
            id=row["id"], name=row["name"], vendor=row["vendor"],
            description=row["description"] or "", logo_path=row["logo_path"] or "",
            website_url=row["website_url"] or "", is_default=bool(row["is_default"]),
        )

    @staticmethod
    def _row_to_industry(row) -> Industry:
        return Industry(
            id=row["id"], name=row["name"], description=row["description"] or "",
            icon_name=row["icon_name"], sort_order=row["sort_order"],
        )

    @staticmethod
    def _row_to_feature(row) -> Feature:
        return Feature(
            id=row["id"], name=row["name"], category=row["category"],
            description=row["description"] or "", data_type=row["data_type"],
        )


class RepositoryFactory:
    """Factory for creating repository instances."""

    @staticmethod
    def create(backend: str = "sqlite", **kwargs) -> AbstractRepository:
        if backend == "sqlite":
            return SQLiteRepository(kwargs.get("db_path", "battlecard.db"))
        if backend == "tidb":
            return TiDBCloudRepository(**kwargs)
        raise ValueError(f"Unknown backend: {backend}")



