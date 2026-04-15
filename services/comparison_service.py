"""Comparison service — orchestrates the comparison workflow."""
from typing import List, Optional

from db.repository import AbstractRepository
from models.entities import ComparisonResult


class ComparisonService:
    """Builds comparison results from repository data."""

    def __init__(self, repo: AbstractRepository):
        self._repo = repo

    def build_comparison(
        self,
        product_b_id: int,
        industry_id: int,
        extra_feature_ids: Optional[List[int]] = None,
    ) -> ComparisonResult:
        product_a = self._repo.get_default_product()
        product_b = self._repo.get_product(product_b_id)
        industry = self._repo.get_industry(industry_id)

        # Get industry features
        industry_features = self._repo.get_features_for_industry(industry_id)

        # Add any user-selected extra features
        if extra_feature_ids:
            existing_ids = {sf.feature.id for sf in industry_features}
            for fid in extra_feature_ids:
                if fid not in existing_ids:
                    self._repo.add_feature_to_industry(industry_id, fid)
            industry_features = self._repo.get_features_for_industry(industry_id)

        # Fetch feature values for both products
        feature_ids = [sf.feature.id for sf in industry_features]
        vals_a = self._repo.get_product_feature_values(product_a.id, feature_ids)
        vals_b = self._repo.get_product_feature_values(product_b.id, feature_ids)

        # Build comparison tuples: (Feature, value_a, value_b, weight)
        feature_comparisons = [
            (sf.feature, vals_a.get(sf.feature.id, "N/A"), vals_b.get(sf.feature.id, "N/A"), sf.weight)
            for sf in industry_features
        ]

        expert_advice = self._repo.get_expert_advice(industry_id, product_a.id, product_b.id)
        case_studies = self._repo.get_case_studies(industry_id, product_a.id)

        return ComparisonResult(
            product_a=product_a,
            product_b=product_b,
            industry=industry,
            feature_comparisons=feature_comparisons,
            expert_advice_list=expert_advice,
            case_studies=case_studies,
        )
