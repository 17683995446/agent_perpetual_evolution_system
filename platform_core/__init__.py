"""
Agent 永续自进化系统 - 平台核心模块

版本: v6.0.0
模块: SaaS平台核心架构
包含: 多租户管理、订阅计费、API市场、开发者门户等核心功能
"""

from .platform_components import (
    Tenant,
    TenantStatus,
    SubscriptionPlan,
    ResourceQuota,
    BillingInfo,
    MultiTenantManager,
    TenantIsolation,
    SharedResourcePool,
    TenantLifecycleManager,
    TenantQuotaEnforcer,
    TenantMigrationManager
)

__all__ = [
    "Tenant",
    "TenantStatus",
    "SubscriptionPlan",
    "ResourceQuota",
    "BillingInfo",
    "MultiTenantManager",
    "TenantIsolation",
    "SharedResourcePool",
    "TenantLifecycleManager",
    "TenantQuotaEnforcer",
    "TenantMigrationManager"
]
