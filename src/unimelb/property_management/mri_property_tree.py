"""
MRI Property Tree Integration — Full Residential & Commercial
==============================================================
Integrates UniMelb campus property management with MRI Software's
Property Tree system. Covers student housing, staff residences,
retail tenancies, commercial leases, and sub-tenant management.

Agents: Lendlease (facility mgmt), JLL (valuation/leasing), MICM (residential)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PropertyType(Enum):
    """Property classification for UniMelb campus estate."""

    RESIDENTIAL_STUDENT = "residential_student"
    RESIDENTIAL_STAFF = "residential_staff"
    RESIDENTIAL_VISITOR = "residential_visitor"
    COMMERCIAL_RETAIL = "commercial_retail"
    COMMERCIAL_OFFICE = "commercial_office"
    COMMERCIAL_LAB = "commercial_lab"
    COMMERCIAL_VENUE = "commercial_venue"
    COMMERCIAL_FOOD_BEVERAGE = "commercial_food_beverage"


class TenantRole(Enum):
    """Tenant and agent role classification."""

    TENANT = "tenant"
    SUB_TENANT = "sub_tenant"
    AGENT_LENDLEASE = "agent_lendlease"
    AGENT_JLL = "agent_jll"
    AGENT_MICM = "agent_micm"
    SUPPLIER = "supplier"
    UNIVERSITY_ADMIN = "university_admin"


class LeaseStatus(Enum):
    """Lease lifecycle states."""

    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    RENEWAL_DUE = "renewal_due"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class MaintenanceStatus(Enum):
    """Maintenance request lifecycle states."""

    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    AWAITING_PARTS = "awaiting_parts"
    COMPLETED = "completed"
    CLOSED = "closed"


class DeploymentEnvironment(Enum):
    """MRI Property Tree deployment environments."""

    ALPHA_DEV = "alpha_dev"         # Development — synthetic data
    BETA_STAGING = "beta_staging"   # Staging — anonymised production clone
    TEST = "test"                   # Automated regression — synthetic + edge cases
    TRAINING = "training"           # Staff training — curated dataset
    DAILY_USE = "daily_use"         # Standard operations — live data
    LIVE_PRODUCTION = "live"        # Real-time production — primary
    BACKUP = "backup"               # Geo-redundant replica — DR


@dataclass
class Property:
    """A single property unit within the UniMelb campus estate."""

    property_id: str
    name: str
    property_type: PropertyType
    address: str
    campus: str = "Parkville"
    floor_area_sqm: float = 0.0
    building: str = ""
    level: str = ""
    unit: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Tenant:
    """A tenant, sub-tenant, or agent in the property management system."""

    tenant_id: str
    name: str
    role: TenantRole
    email: str = ""
    phone: str = ""
    company: str = ""
    abn: str = ""  # Australian Business Number
    entra_id: str = ""  # Microsoft Entra ID for SSO
    properties: list[str] = field(default_factory=list)  # property_ids
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Lease:
    """A lease agreement between UniMelb and a tenant."""

    lease_id: str
    property_id: str
    tenant_id: str
    lease_type: PropertyType
    status: LeaseStatus = LeaseStatus.DRAFT
    start_date: datetime | None = None
    end_date: datetime | None = None
    rent_amount_aud: float = 0.0
    rent_frequency: str = "monthly"  # weekly | fortnightly | monthly | quarterly
    bond_amount_aud: float = 0.0
    conditions: list[str] = field(default_factory=list)
    managing_agent: TenantRole | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MaintenanceRequest:
    """A maintenance request for a campus property."""

    request_id: str
    property_id: str
    tenant_id: str
    description: str
    status: MaintenanceStatus = MaintenanceStatus.OPEN
    priority: str = "medium"  # low | medium | high | urgent
    assigned_agent: TenantRole | None = None
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: datetime | None = None
    cost_aud: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class MRIPropertyTreeClient:
    """
    MRI Property Tree API Client for UniMelb AI Platform.

    Provides CRUD operations for properties, tenants, leases, and
    maintenance across all deployment environments (Alpha → Production).

    Integration points:
    - Azure Service Bus for event-driven sync
    - Microsoft Teams for agent/tenant notifications
    - Power BI for lease analytics
    - UniMelb AI Copilot for property assistance
    """

    def __init__(
        self,
        api_endpoint: str = "",
        api_key: str = "",
        environment: DeploymentEnvironment = DeploymentEnvironment.ALPHA_DEV,
    ):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.environment = environment
        self._properties: dict[str, Property] = {}
        self._tenants: dict[str, Tenant] = {}
        self._leases: dict[str, Lease] = {}
        self._maintenance: dict[str, MaintenanceRequest] = {}

    # ── Property Operations ──────────────────────────────────────────

    def register_property(self, prop: Property) -> Property:
        """Register a new property in the system."""
        self._properties[prop.property_id] = prop
        return prop

    def get_property(self, property_id: str) -> Property | None:
        """Retrieve a property by ID."""
        return self._properties.get(property_id)

    def list_properties(
        self,
        property_type: PropertyType | None = None,
        campus: str | None = None,
    ) -> list[Property]:
        """List properties, optionally filtered by type and campus."""
        results = list(self._properties.values())
        if property_type:
            results = [p for p in results if p.property_type == property_type]
        if campus:
            results = [p for p in results if p.campus == campus]
        return results

    # ── Tenant Operations ────────────────────────────────────────────

    def register_tenant(self, tenant: Tenant) -> Tenant:
        """Register a new tenant, sub-tenant, or agent."""
        self._tenants[tenant.tenant_id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant | None:
        """Retrieve a tenant by ID."""
        return self._tenants.get(tenant_id)

    def list_tenants(
        self,
        role: TenantRole | None = None,
    ) -> list[Tenant]:
        """List tenants, optionally filtered by role."""
        results = list(self._tenants.values())
        if role:
            results = [t for t in results if t.role == role]
        return results

    def list_agents(self) -> list[Tenant]:
        """List all property management agents (Lendlease, JLL, MICM)."""
        agent_roles = {
            TenantRole.AGENT_LENDLEASE,
            TenantRole.AGENT_JLL,
            TenantRole.AGENT_MICM,
        }
        return [t for t in self._tenants.values() if t.role in agent_roles]

    # ── Lease Operations ─────────────────────────────────────────────

    def create_lease(self, lease: Lease) -> Lease:
        """Create a new lease agreement."""
        self._leases[lease.lease_id] = lease
        return lease

    def get_lease(self, lease_id: str) -> Lease | None:
        """Retrieve a lease by ID."""
        return self._leases.get(lease_id)

    def list_leases(
        self,
        status: LeaseStatus | None = None,
        property_type: PropertyType | None = None,
    ) -> list[Lease]:
        """List leases, optionally filtered by status and type."""
        results = list(self._leases.values())
        if status:
            results = [le for le in results if le.status == status]
        if property_type:
            results = [le for le in results if le.lease_type == property_type]
        return results

    def get_expiring_leases(self, within_days: int = 90) -> list[Lease]:
        """Get leases expiring within the given number of days."""
        cutoff = datetime.now()
        results = []
        for lease in self._leases.values():
            if (
                lease.status == LeaseStatus.ACTIVE
                and lease.end_date
                and (lease.end_date - cutoff).days <= within_days
            ):
                results.append(lease)
        return results

    # ── Maintenance Operations ───────────────────────────────────────

    def create_maintenance_request(
        self, request: MaintenanceRequest
    ) -> MaintenanceRequest:
        """Create a new maintenance request."""
        self._maintenance[request.request_id] = request
        return request

    def get_maintenance_request(
        self, request_id: str
    ) -> MaintenanceRequest | None:
        """Retrieve a maintenance request by ID."""
        return self._maintenance.get(request_id)

    def list_maintenance_requests(
        self,
        status: MaintenanceStatus | None = None,
        property_id: str | None = None,
    ) -> list[MaintenanceRequest]:
        """List maintenance requests with optional filters."""
        results = list(self._maintenance.values())
        if status:
            results = [m for m in results if m.status == status]
        if property_id:
            results = [m for m in results if m.property_id == property_id]
        return results

    # ── Analytics & Reporting ────────────────────────────────────────

    def get_portfolio_summary(self) -> dict[str, Any]:
        """Generate a portfolio summary for dashboards and Power BI."""
        total_properties = len(self._properties)
        total_leases = len(self._leases)
        active_leases = len(self.list_leases(status=LeaseStatus.ACTIVE))
        expiring_soon = len(self.get_expiring_leases(within_days=90))
        open_maintenance = len(
            self.list_maintenance_requests(status=MaintenanceStatus.OPEN)
        )

        total_rent = sum(
            le.rent_amount_aud
            for le in self._leases.values()
            if le.status == LeaseStatus.ACTIVE
        )

        residential = len(
            [
                p
                for p in self._properties.values()
                if p.property_type.value.startswith("residential")
            ]
        )
        commercial = len(
            [
                p
                for p in self._properties.values()
                if p.property_type.value.startswith("commercial")
            ]
        )

        return {
            "total_properties": total_properties,
            "residential_count": residential,
            "commercial_count": commercial,
            "total_leases": total_leases,
            "active_leases": active_leases,
            "expiring_within_90_days": expiring_soon,
            "open_maintenance_requests": open_maintenance,
            "total_monthly_rent_aud": total_rent,
            "agents": [
                {"name": a.company, "role": a.role.value}
                for a in self.list_agents()
            ],
            "environment": self.environment.value,
        }

    # ── Environment Management ───────────────────────────────────────

    def switch_environment(self, env: DeploymentEnvironment) -> None:
        """Switch deployment environment (Alpha → Beta → Production)."""
        self.environment = env

    def get_environment_info(self) -> dict[str, Any]:
        """Get current environment details."""
        env_configs = {
            DeploymentEnvironment.ALPHA_DEV: {
                "data_type": "synthetic",
                "access": "developers_only",
                "language_stack": "Python/TypeScript",
                "database": "SQLite",
            },
            DeploymentEnvironment.BETA_STAGING: {
                "data_type": "anonymised_production_clone",
                "access": "dev_qa_select_users",
                "language_stack": "C#/.NET + TypeScript",
                "database": "Azure SQL (staging)",
            },
            DeploymentEnvironment.TEST: {
                "data_type": "synthetic_edge_cases",
                "access": "ci_cd_pipeline",
                "language_stack": "All",
                "database": "Ephemeral",
            },
            DeploymentEnvironment.TRAINING: {
                "data_type": "curated_training_dataset",
                "access": "onboarding_users",
                "language_stack": "All",
                "database": "Training DB",
            },
            DeploymentEnvironment.DAILY_USE: {
                "data_type": "live_production",
                "access": "authorised_users",
                "language_stack": "C#/.NET + C/C++ core",
                "database": "Azure SQL",
            },
            DeploymentEnvironment.LIVE_PRODUCTION: {
                "data_type": "live_primary",
                "access": "all_users_per_rbac",
                "language_stack": "C#/.NET + C/C++ core",
                "database": "Azure SQL HA",
            },
            DeploymentEnvironment.BACKUP: {
                "data_type": "geo_redundant_replica",
                "access": "dr_team_automated",
                "language_stack": "N/A",
                "database": "Azure SQL Geo-replica",
            },
        }
        return {
            "environment": self.environment.value,
            **env_configs.get(self.environment, {}),
        }
