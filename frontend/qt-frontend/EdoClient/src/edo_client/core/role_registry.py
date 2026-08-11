"""Role Registry - Manages user roles and permissions."""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional


class Permission(Enum):
    """Available permissions in the EDO system."""
    
    VIEW_DATASETS = auto()
    IMPORT_DATASETS = auto()
    EDIT_METADATA = auto()
    RUN_VALIDATION = auto()
    ANNOTATE_RESOURCES = auto()
    RUN_SEMANTIC_EXPANSION = auto()
    RUN_INGESTION_OEP = auto()
    RUN_INGESTION_HKG = auto()
    ACCESS_INGESTION_WORKFLOW = auto()
    MANAGE_USERS = auto()
    ADMIN_ACCESS = auto()


@dataclass
class RolePolicy:
    """Defines permissions for a specific role."""
    
    role_id: str
    display_name: str
    description: str
    permissions: Set[Permission] = field(default_factory=set)
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if this role has a specific permission."""
        return permission in self.permissions


class RoleRegistry:
    """Central registry for roles and policies."""
    
    def __init__(self) -> None:
        self._roles: Dict[str, RolePolicy] = {}
        self._default_role: Optional[str] = None
        self._setup_builtin_roles()
    
    def _setup_builtin_roles(self) -> None:
        """Register built-in roles with their permissions."""
        
        # Guest Viewer - minimal read-only access
        guest = RolePolicy(
            role_id="guest_viewer",
            display_name="Guest Viewer",
            description="Read-only access to public datasets",
            permissions={Permission.VIEW_DATASETS}
        )
        self.register_role(guest)
        
        # Research Fellow - standard researcher access
        fellow = RolePolicy(
            role_id="research_fellow",
            display_name="Research Fellow",
            description="Full research access with annotation capabilities",
            permissions={
                Permission.VIEW_DATASETS,
                Permission.IMPORT_DATASETS,
                Permission.EDIT_METADATA,
                Permission.RUN_VALIDATION,
                Permission.ANNOTATE_RESOURCES,
                Permission.RUN_SEMANTIC_EXPANSION,
            }
        )
        self.register_role(fellow)
        self._default_role = "research_fellow"
        
        # Data Steward - includes ingestion workflows
        steward = RolePolicy(
            role_id="data_steward",
            display_name="Data Steward",
            description="Manages data ingestion and workflow orchestration",
            permissions={
                Permission.VIEW_DATASETS,
                Permission.IMPORT_DATASETS,
                Permission.EDIT_METADATA,
                Permission.RUN_VALIDATION,
                Permission.ANNOTATE_RESOURCES,
                Permission.RUN_SEMANTIC_EXPANSION,
                Permission.RUN_INGESTION_OEP,
                Permission.RUN_INGESTION_HKG,
                Permission.ACCESS_INGESTION_WORKFLOW,
            }
        )
        self.register_role(steward)
        
        # Admin - full access
        admin = RolePolicy(
            role_id="admin",
            display_name="Administrator",
            description="Full system access",
            permissions=set(Permission)
        )
        self.register_role(admin)
    
    def register_role(self, policy: RolePolicy) -> None:
        """Register a role policy."""
        self._roles[policy.role_id] = policy
    
    def get_policy(self, role_id: str) -> Optional[RolePolicy]:
        """Get policy for a specific role."""
        return self._roles.get(role_id)
    
    def get_effective_policy(self, role_ids: List[str]) -> Optional[RolePolicy]:
        """Get combined policy for multiple roles (union of permissions)."""
        if not role_ids:
            return self.get_policy(self._default_role) if self._default_role else None
        
        combined_permissions: Set[Permission] = set()
        display_name = "Custom Role"
        
        for role_id in role_ids:
            policy = self._roles.get(role_id)
            if policy:
                combined_permissions.update(policy.permissions)
                display_name = policy.display_name
        
        if not combined_permissions:
            return self.get_policy(self._default_role) if self._default_role else None
        
        return RolePolicy(
            role_id="+".join(role_ids),
            display_name=display_name,
            description="Combined role policy",
            permissions=combined_permissions
        )
    
    @property
    def default_role(self) -> Optional[str]:
        """Get the default role ID."""
        return self._default_role
    
    @property
    def available_roles(self) -> List[str]:
        """Get list of all available role IDs."""
        return list(self._roles.keys())


# Global registry instance
_registry: Optional[RoleRegistry] = None


def get_role_registry() -> RoleRegistry:
    """Get or create the global role registry."""
    global _registry
    if _registry is None:
        _registry = RoleRegistry()
    return _registry
