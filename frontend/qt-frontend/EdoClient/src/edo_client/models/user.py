"""
User Models - User profiles and roles for Abstract UI trees

Used across all Abstract Model Trees for authentication and authorization
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class UserRoleType(Enum):
    """Standard EDO user roles from MDUID specification."""
    GUEST_VIEWER = "guest_viewer"
    RESEARCH_FELLOW = "research_fellow"
    DATA_STEWARD = "data_steward"
    ADMIN = "admin"


@dataclass
class UserProfile:
    """
    User profile information.
    
    Used in AbstractUI: ViewDatasetDetail → Sidebar → AuthorProfileCard
    and AbstractUI: SystemAdministration → UsersAndRoles
    """
    user_id: str
    username: str
    email: str
    display_name: str
    orcid: Optional[str] = None
    institution: Optional[str] = None
    ror_id: Optional[str] = None
    role: UserRoleType = UserRoleType.GUEST_VIEWER
    additional_roles: List[UserRoleType] = field(default_factory=list)
    
    # Profile metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    # Statistics
    datasets_submitted: int = 0
    datasets_reviewed: int = 0
    last_activity: Optional[datetime] = None
    
    @property
    def has_orcid(self) -> bool:
        return self.orcid is not None
    
    @property
    def has_institution(self) -> bool:
        return self.institution is not None
    
    @property
    def all_roles(self) -> List[UserRoleType]:
        """Get all roles including primary and additional."""
        return [self.role] + self.additional_roles
    
    def can_perform_action(self, action: str) -> bool:
        """Check if user can perform a specific action based on role."""
        # Role-based action permissions (simplified)
        role_permissions = {
            UserRoleType.GUEST_VIEWER: {"browse", "view", "search", "download_open"},
            UserRoleType.RESEARCH_FELLOW: {
                "browse", "view", "search", "download_open", 
                "create_metadata", "edit_own", "submit", "annotate"
            },
            UserRoleType.DATA_STEWARD: {
                "browse", "view", "search", "download_open",
                "create_metadata", "edit_all", "review", "approve", "request_revisions"
            },
            UserRoleType.ADMIN: {"*"}  # All permissions
        }
        
        for role in self.all_roles:
            perms = role_permissions.get(role, set())
            if "*" in perms or action in perms:
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "userId": self.user_id,
            "username": self.username,
            "email": self.email,
            "displayName": self.display_name,
            "orcid": self.orcid,
            "institution": self.institution,
            "rorId": self.ror_id,
            "role": self.role.value,
            "additionalRoles": [r.value for r in self.additional_roles],
            "createdAt": self.created_at.isoformat(),
            "lastLogin": self.last_login.isoformat() if self.last_login else None,
            "isActive": self.is_active,
            "datasetsSubmitted": self.datasets_submitted,
            "datasetsReviewed": self.datasets_reviewed,
        }


@dataclass
class UserRole:
    """
    Role definition with permissions.
    
    Corresponds to role-based access control matrix in Abstract Model Trees
    """
    role_id: str
    display_name: str
    description: str
    permissions: List[str] = field(default_factory=list)
    ui_components: List[str] = field(default_factory=list)
    
    # Access control for Abstract UI components
    can_browse_catalog: bool = True
    can_view_detail: bool = True
    can_create_metadata: bool = False
    can_edit_own_metadata: bool = False
    can_edit_all_metadata: bool = False
    can_review_metadata: bool = False
    can_configure_platforms: bool = False
    can_manage_plugins: bool = False
    can_manage_users: bool = False
    can_access_system_admin: bool = False
    
    @classmethod
    def guest_viewer(cls) -> "UserRole":
        """Create default guest viewer role."""
        return cls(
            role_id="guest_viewer",
            display_name="Guest Viewer",
            description="Read-only access to public datasets",
            permissions=["view_datasets"],
            ui_components=["BrowseCatalog", "ViewDatasetDetail"],
            can_browse_catalog=True,
            can_view_detail=True,
        )
    
    @classmethod
    def research_fellow(cls) -> "UserRole":
        """Create default research fellow role."""
        return cls(
            role_id="research_fellow",
            display_name="Research Fellow",
            description="Full research access with annotation capabilities",
            permissions=[
                "view_datasets", "import_datasets", "edit_metadata",
                "run_validation", "annotate_resources", "run_semantic_expansion"
            ],
            ui_components=["BrowseCatalog", "ViewDatasetDetail", "CreateMetadataWizard", "EditMetadata"],
            can_browse_catalog=True,
            can_view_detail=True,
            can_create_metadata=True,
            can_edit_own_metadata=True,
        )
    
    @classmethod
    def data_steward(cls) -> "UserRole":
        """Create default data steward role."""
        return cls(
            role_id="data_steward",
            display_name="Data Steward",
            description="Manages data ingestion and workflow orchestration",
            permissions=[
                "view_datasets", "import_datasets", "edit_metadata",
                "run_validation", "annotate_resources", "run_semantic_expansion",
                "run_ingestion_oep", "run_ingestion_hkg", "access_ingestion_workflow"
            ],
            ui_components=[
                "BrowseCatalog", "ViewDatasetDetail", "CreateMetadataWizard",
                "EditMetadata", "ReviewDashboard", "ReviewDetail"
            ],
            can_browse_catalog=True,
            can_view_detail=True,
            can_create_metadata=True,
            can_edit_own_metadata=True,
            can_edit_all_metadata=True,
            can_review_metadata=True,
            can_configure_platforms=True,
        )
    
    @classmethod
    def admin(cls) -> "UserRole":
        """Create default admin role."""
        return cls(
            role_id="admin",
            display_name="Administrator",
            description="Full system access",
            permissions=["*"],
            ui_components=["*"],
            can_browse_catalog=True,
            can_view_detail=True,
            can_create_metadata=True,
            can_edit_own_metadata=True,
            can_edit_all_metadata=True,
            can_review_metadata=True,
            can_configure_platforms=True,
            can_manage_plugins=True,
            can_manage_users=True,
            can_access_system_admin=True,
        )
    
    @classmethod
    def get_builtin_role(cls, role_id: str) -> Optional["UserRole"]:
        """Get a built-in role by ID."""
        role_map = {
            "guest_viewer": cls.guest_viewer,
            "research_fellow": cls.research_fellow,
            "data_steward": cls.data_steward,
            "admin": cls.admin,
        }
        factory = role_map.get(role_id)
        return factory() if factory else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "roleId": self.role_id,
            "displayName": self.display_name,
            "description": self.description,
            "permissions": self.permissions,
            "uiComponents": self.ui_components,
            "canBrowseCatalog": self.can_browse_catalog,
            "canViewDetail": self.can_view_detail,
            "canCreateMetadata": self.can_create_metadata,
            "canEditOwnMetadata": self.can_edit_own_metadata,
            "canEditAllMetadata": self.can_edit_all_metadata,
            "canReviewMetadata": self.can_review_metadata,
            "canConfigurePlatforms": self.can_configure_platforms,
            "canManagePlugins": self.can_manage_plugins,
            "canManageUsers": self.can_manage_users,
            "canAccessSystemAdmin": self.can_access_system_admin,
        }


@dataclass
class SessionContext:
    """
    Current user session context.
    
    Provides role-based UI component visibility across all Abstract Models
    """
    user: UserProfile
    current_role: UserRole
    session_id: str
    login_time: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    
    # UI state
    visible_components: List[str] = field(default_factory=list)
    allowed_actions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize visible components and actions based on role."""
        self.visible_components = self.current_role.ui_components
        self.allowed_actions = self.current_role.permissions
    
    def can_access_component(self, component_name: str) -> bool:
        """Check if user can access a specific UI component."""
        if "*" in self.visible_components:
            return True
        return component_name in self.visible_components
    
    def can_perform_action(self, action: str) -> bool:
        """Check if user can perform a specific action."""
        if "*" in self.allowed_actions:
            return True
        return action in self.allowed_actions
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
        self.user.last_activity = datetime.now()
    
    def switch_role(self, new_role: UserRole) -> bool:
        """
        Switch to a different role if user has it.
        Returns True if successful.
        """
        if new_role.role_id == self.user.role.value:
            self.current_role = new_role
            self.__post_init__()
            return True
        
        if new_role.role_id in [r.value for r in self.user.additional_roles]:
            self.current_role = new_role
            self.__post_init__()
            return True
        
        return False
