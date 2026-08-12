"""
Platform Models - Abstract Model Tree 7: PlatformConfiguration

Supports CF2, CF4 for FAIR Phase: SHARE
Primary Roles: admin, data_steward (limited)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from enum import Enum


class AuthType(Enum):
    """Authentication types for platform connections."""
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BASIC = "basic"
    NONE = "none"


class ConnectionStatus(Enum):
    """Platform connection status."""
    CONNECTED = "connected"
    ERROR = "error"
    NOT_CONFIGURED = "not-configured"
    TESTING = "testing"


class SchemaCompatibility(Enum):
    """Schema mapping compatibility status."""
    COMPATIBLE = "compatible"
    REQUIRES_MAPPING = "requires_mapping"
    INCOMPATIBLE = "incompatible"


@dataclass
class CredentialVault:
    """Secure credential storage for platform authentication."""
    credential_id: str
    platform_id: str
    auth_type: AuthType
    
    # Encrypted fields (in real implementation)
    username: Optional[str] = None
    api_key: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    is_valid: bool = True
    
    def needs_refresh(self) -> bool:
        """Check if OAuth token needs refresh."""
        if not self.token_expires_at:
            return False
        # Refresh if expires within 5 minutes
        from datetime import timedelta
        return datetime.now() + timedelta(minutes=5) > self.token_expires_at
    
    def clear_tokens(self) -> None:
        """Clear sensitive tokens."""
        self.access_token = None
        self.refresh_token = None


@dataclass
class FieldMapping:
    """Single field mapping between source and target schemas."""
    source_field: str
    target_field: str
    transformation_rule: Optional[str] = None
    is_required: bool = False
    default_value: Optional[Any] = None
    validation_rules: List[str] = field(default_factory=list)
    
    def apply_transformation(self, value: Any) -> Any:
        """Apply transformation rule to value."""
        if not self.transformation_rule:
            return value
        
        # Simple transformation rules (expand as needed)
        if self.transformation_rule == "uppercase":
            return str(value).upper() if value else value
        elif self.transformation_rule == "lowercase":
            return str(value).lower() if value else value
        elif self.transformation_rule == "trim":
            return str(value).strip() if value else value
        elif self.transformation_rule.startswith("prefix:"):
            prefix = self.transformation_rule[7:]
            return f"{prefix}{value}" if value else value
        elif self.transformation_rule.startswith("suffix:"):
            suffix = self.transformation_rule[7:]
            return f"{value}{suffix}" if value else value
        
        return value


@dataclass
class PlatformMapping:
    """
    Schema mapping configuration between EDO internal and platform-specific schema.
    
    Corresponds to AbstractUI: PlatformConfiguration → PlatformCard → ConfigurationSection → SchemaMapping
    """
    mapping_id: str
    platform_id: str
    source_schema: str  # EDO internal schema
    target_schema: str  # Platform-specific schema
    compatibility: SchemaCompatibility = SchemaCompatibility.REQUIRES_MAPPING
    
    field_mappings: List[FieldMapping] = field(default_factory=list)
    validation_rules: List[str] = field(default_factory=list)
    
    # Mapping statistics
    mapped_fields_count: int = 0
    unmapped_required_fields: List[str] = field(default_factory=list)
    last_validated: Optional[datetime] = None
    
    def add_mapping(self, mapping: FieldMapping) -> None:
        """Add a field mapping."""
        self.field_mappings.append(mapping)
        self.mapped_fields_count = len(self.field_mappings)
    
    def get_mapping(self, source_field: str) -> Optional[FieldMapping]:
        """Get mapping for a source field."""
        for m in self.field_mappings:
            if m.source_field == source_field:
                return m
        return None
    
    def validate_mapping(self, source_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that all required target fields can be mapped.
        Returns (is_valid, list_of_errors).
        """
        errors = []
        
        # Check required mappings
        for mapping in self.field_mappings:
            if mapping.is_required and mapping.source_field not in source_data:
                if mapping.default_value is None:
                    errors.append(
                        f"Required field '{mapping.target_field}' has no source or default value"
                    )
        
        self.unmapped_required_fields = [
            m.target_field for m in self.field_mappings 
            if m.is_required and m.source_field not in source_data
        ]
        
        self.last_validated = datetime.now()
        return len(errors) == 0, errors
    
    def transform_data(self, source_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform source data to target schema format."""
        target_data = {}
        
        for mapping in self.field_mappings:
            if mapping.source_field in source_data:
                value = source_data[mapping.source_field]
                transformed = mapping.apply_transformation(value)
                target_data[mapping.target_field] = transformed
            elif mapping.default_value is not None:
                target_data[mapping.target_field] = mapping.default_value
        
        return target_data
    
    def get_completeness_score(self) -> float:
        """Calculate mapping completeness (0.0 to 1.0)."""
        if not self.field_mappings:
            return 0.0
        
        # Consider mapping complete if all required fields are mapped
        required_mappings = [m for m in self.field_mappings if m.is_required]
        if not required_mappings:
            return 1.0
        
        mapped_required = sum(
            1 for m in required_mappings 
            if m.source_field or m.default_value is not None
        )
        return mapped_required / len(required_required)


@dataclass
class PublicationDefaults:
    """Default publication settings for a platform."""
    default_license: str = "CC-BY-4.0"
    default_access_type: str = "open"
    auto_publish: bool = False
    embargo_period_days: int = 0
    default_metadata_template: Optional[str] = None


@dataclass
class PlatformConfig:
    """
    Complete platform configuration.
    
    Corresponds to AbstractUI: PlatformConfiguration → PlatformList → PlatformCard
    """
    platform_id: str
    platform_name: str
    domain: Optional[str] = None
    description: Optional[str] = None
    
    # Connection
    api_endpoint: Optional[str] = None
    auth_type: AuthType = AuthType.NONE
    credential_id: Optional[str] = None
    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONFIGURED
    last_connection_test: Optional[datetime] = None
    connection_error: Optional[str] = None
    
    # Plugin info
    plugin_version: Optional[str] = None
    plugin_installed: bool = False
    
    # Schema mapping
    mapping: Optional[PlatformMapping] = None
    
    # Publication defaults
    defaults: PublicationDefaults = field(default_factory=PublicationDefaults)
    
    # State
    is_enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Usage statistics
    publications_count: int = 0
    last_publication: Optional[datetime] = None
    
    def test_connection(self) -> bool:
        """Test platform connection (placeholder for real implementation)."""
        self.connection_status = ConnectionStatus.TESTING
        
        # In real implementation, would make actual API call
        if not self.api_endpoint:
            self.connection_status = ConnectionStatus.ERROR
            self.connection_error = "No API endpoint configured"
            return False
        
        if self.auth_type != AuthType.NONE and not self.credential_id:
            self.connection_status = ConnectionStatus.ERROR
            self.connection_error = "No credentials configured"
            return False
        
        self.connection_status = ConnectionStatus.CONNECTED
        self.connection_error = None
        self.last_connection_test = datetime.now()
        return True
    
    def get_schema_compatibility(self) -> SchemaCompatibility:
        """Get schema compatibility status."""
        if not self.mapping:
            return SchemaCompatibility.NOT_CONFIGURED
        return self.mapping.compatibility
    
    def can_publish(self) -> bool:
        """Check if platform is ready for publication."""
        return (
            self.is_enabled and
            self.connection_status == ConnectionStatus.CONNECTED and
            self.mapping is not None and
            self.plugin_installed
        )
    
    def update_timestamp(self) -> None:
        """Update the modification timestamp."""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for UI serialization."""
        return {
            "platformId": self.platform_id,
            "platformName": self.platform_name,
            "domain": self.domain,
            "description": self.description,
            "apiEndpoint": self.api_endpoint,
            "authType": self.auth_type.value,
            "connectionStatus": self.connection_status.value,
            "pluginVersion": self.plugin_version,
            "pluginInstalled": self.plugin_installed,
            "isEnabled": self.is_enabled,
            "publicationsCount": self.publications_count,
            "lastPublication": self.last_publication.isoformat() if self.last_publication else None,
            "schemaCompatibility": self.get_schema_compatibility().value if self.mapping else None,
            "defaultLicense": self.defaults.default_license,
            "defaultAccessType": self.defaults.default_access_type,
            "autoPublish": self.defaults.auto_publish,
        }


@dataclass
class PluginInfo:
    """Information about a platform plugin."""
    plugin_id: str
    name: str
    version: str
    description: str
    author: str
    platform_type: str
    min_edo_version: str
    is_installed: bool = False
    is_compatible: bool = True
    installation_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pluginId": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "platformType": self.platform_type,
            "minEdoVersion": self.min_edo_version,
            "isInstalled": self.is_installed,
            "isCompatible": self.is_compatible,
        }


@dataclass
class PlatformConfigurationModel:
    """
    Complete platform configuration management model.
    
    Corresponds to AbstractUI: PlatformConfiguration
    """
    platforms: List[PlatformConfig] = field(default_factory=list)
    plugins: List[PluginInfo] = field(default_factory=list)
    isLoading: bool = False
    error: Optional[str] = None
    
    # Filter state
    show_only_enabled: bool = False
    show_only_connected: bool = False
    domain_filter: Optional[str] = None
    
    def add_platform(self, platform: PlatformConfig) -> None:
        """Add a platform configuration."""
        self.platforms.append(platform)
    
    def get_platform(self, platform_id: str) -> Optional[PlatformConfig]:
        """Get a specific platform by ID."""
        for p in self.platforms:
            if p.platform_id == platform_id:
                return p
        return None
    
    def remove_platform(self, platform_id: str) -> bool:
        """Remove a platform. Returns True if successful."""
        platform = self.get_platform(platform_id)
        if platform:
            self.platforms.remove(platform)
            return True
        return False
    
    def get_filtered_platforms(self) -> List[PlatformConfig]:
        """Get platforms filtered by current settings."""
        filtered = self.platforms.copy()
        
        if self.show_only_enabled:
            filtered = [p for p in filtered if p.is_enabled]
        
        if self.show_only_connected:
            filtered = [
                p for p in filtered 
                if p.connection_status == ConnectionStatus.CONNECTED
            ]
        
        if self.domain_filter:
            filtered = [p for p in filtered if p.domain == self.domain_filter]
        
        return filtered
    
    def get_available_domains(self) -> List[str]:
        """Get list of unique domains from configured platforms."""
        domains = set()
        for p in self.platforms:
            if p.domain:
                domains.add(p.domain)
        return sorted(list(domains))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform configuration statistics."""
        total = len(self.platforms)
        enabled = sum(1 for p in self.platforms if p.is_enabled)
        connected = sum(1 for p in self.platforms if p.connection_status == ConnectionStatus.CONNECTED)
        installed_plugins = sum(1 for p in self.plugins if p.is_installed)
        
        return {
            "totalPlatforms": total,
            "enabledPlatforms": enabled,
            "connectedPlatforms": connected,
            "installedPlugins": installed_plugins,
            "totalPublications": sum(p.publications_count for p in self.platforms),
        }
    
    def test_all_connections(self) -> Dict[str, bool]:
        """Test connections for all platforms. Returns map of platform_id → success."""
        results = {}
        for platform in self.platforms:
            results[platform.platform_id] = platform.test_connection()
        return results
    
    def get_compatible_platforms_for_schema(self, schema_name: str) -> List[PlatformConfig]:
        """Get platforms compatible with a given metadata schema."""
        compatible = []
        for p in self.platforms:
            if p.mapping and p.mapping.source_schema == schema_name:
                if p.mapping.compatibility in [
                    SchemaCompatibility.COMPATIBLE,
                    SchemaCompatibility.REQUIRES_MAPPING
                ]:
                    compatible.append(p)
        return compatible
