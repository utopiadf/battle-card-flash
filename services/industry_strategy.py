"""Strategy pattern for industry-specific comparison logic."""
from abc import ABC, abstractmethod
from typing import List


class ComparisonStrategy(ABC):
    """Base strategy for industry-specific comparison behavior."""

    @abstractmethod
    def get_priority_categories(self) -> List[str]:
        """Return feature categories in priority order for this industry."""
        ...

    @abstractmethod
    def get_llm_context_prompt(self) -> str:
        """Return industry-specific context for the LLM prompt."""
        ...


class AIAgentStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["AI/ML", "Performance", "Scalability", "Operations"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on AI agent workloads: vector similarity search, "
            "RAG pipeline support, real-time inference serving, "
            "JSON document handling, and horizontal scalability "
            "for embedding storage. Evaluate HTAP capabilities "
            "for combining transactional and analytical AI operations."
        )


class GamingStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["Performance", "Reliability", "Scalability", "Cost"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on online gaming backend requirements: "
            "ultra-low read/write latency for player state, "
            "high throughput for concurrent player actions, "
            "global distribution for multi-region matchmaking, "
            "and automatic failover for zero-downtime gameplay."
        )


class ECommerceStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["SQL Compatibility", "Performance", "Scalability", "Reliability"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on e-commerce platform needs: ACID transactions "
            "for order processing and inventory management, "
            "horizontal scaling for flash sale traffic spikes, "
            "real-time analytics for sales dashboards (HTAP), "
            "and MySQL compatibility for existing application migration."
        )


class FinancialServicesStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["Reliability", "SQL Compatibility", "Operations", "Performance"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on financial system requirements: strong consistency "
            "and distributed ACID transactions for money movement, "
            "RPO=0 for zero data loss, multi-region deployment "
            "for disaster recovery, encryption and compliance, "
            "and audit trail capabilities."
        )


class SaaSMultiTenantStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["Scalability", "SQL Compatibility", "Operations", "Cost"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on multi-tenant SaaS requirements: elastic scaling "
            "to handle varying tenant workloads, tenant data isolation, "
            "cost-efficient resource sharing, managed service options "
            "to reduce operational burden, and MySQL compatibility "
            "for broad developer ecosystem support."
        )


class IoTTimeSeriesStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["Performance", "Scalability", "Operations", "Cost"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on IoT and time-series workloads: sustained high "
            "write throughput for sensor data ingestion, automatic "
            "sharding for time-partitioned data, HTAP for real-time "
            "analytics on streaming data, and change data capture "
            "for downstream processing pipelines."
        )


class RetailStrategy(ComparisonStrategy):
    def get_priority_categories(self) -> List[str]:
        return ["Performance", "SQL Compatibility", "Scalability", "Reliability"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Focus on retail system requirements: real-time inventory "
            "tracking across stores and warehouses, low-latency POS "
            "transactions, omnichannel analytics for sales and supply "
            "chain, ACID guarantees for stock management, and horizontal "
            "scaling for seasonal traffic spikes."
        )


class GenericStrategy(ComparisonStrategy):
    """Fallback strategy with equal weight across all categories."""

    def get_priority_categories(self) -> List[str]:
        return ["Performance", "Scalability", "SQL Compatibility", "Reliability", "Operations", "Cost", "AI/ML"]

    def get_llm_context_prompt(self) -> str:
        return (
            "Provide a balanced comparison across all dimensions: "
            "performance, scalability, SQL compatibility, reliability, "
            "operational ease, cost, and AI/ML capabilities."
        )


class StrategyFactory:
    """Factory for creating industry-specific comparison strategies."""

    _registry = {
        "AI": AIAgentStrategy,
        "Gaming": GamingStrategy,
        "eCommerce": ECommerceStrategy,
        "Fintech": FinancialServicesStrategy,
        "SaaS": SaaSMultiTenantStrategy,
        "Retail": RetailStrategy,
    }

    @classmethod
    def create(cls, industry_name: str) -> ComparisonStrategy:
        strategy_cls = cls._registry.get(industry_name, GenericStrategy)
        return strategy_cls()

