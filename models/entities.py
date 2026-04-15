"""Data model entities for Battle Card Flash."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Product:
    id: int
    name: str
    vendor: str
    description: str = ""
    logo_path: str = ""
    website_url: str = ""
    is_default: bool = False


@dataclass
class Industry:
    id: int
    name: str
    description: str = ""
    icon_name: str = "CATEGORY"
    sort_order: int = 0


@dataclass
class Feature:
    id: int
    name: str
    category: str
    description: str = ""
    data_type: str = "text"


@dataclass
class IndustryFeature:
    feature: Feature
    weight: float = 1.0
    sort_order: int = 0


@dataclass
class ProductFeatureValue:
    product: Product
    feature: Feature
    value: str
    source: str = ""


@dataclass
class ExpertAdvice:
    id: int
    industry_id: int
    product_a_id: int
    product_b_id: int
    advice_text: str
    author: str = ""


@dataclass
class CaseStudy:
    id: int
    industry_id: int
    product_id: int
    title: str
    customer: str
    summary: str
    results: str = ""
    source_url: str = ""


@dataclass
class ComparisonResult:
    product_a: Product
    product_b: Product
    industry: Industry
    feature_comparisons: List[tuple] = field(default_factory=list)
    expert_advice_list: List[ExpertAdvice] = field(default_factory=list)
    case_studies: List[CaseStudy] = field(default_factory=list)
    llm_summary: str = ""
