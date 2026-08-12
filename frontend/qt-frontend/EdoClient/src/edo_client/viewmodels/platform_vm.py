"""
Platform View Model - Abstract Model Tree 7: PlatformConfiguration

ViewModel for PyQt/QML binding following MDUID specification.
Supports CF2, CF4 for FAIR Phase: SHARE
Primary Roles: admin, data_steward (limited)
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from PyQt6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    QVariant,
    pyqtSignal,
    pyqtSlot,
)

from ..models.platform import (
    AuthType,
    ConnectionStatus,
    FieldMapping,
    PlatformConfig,
    PlatformConfigurationModel,
    PlatformMapping,
)


class PlatformListModel(QAbstractListModel):
    """QML-compatible list model for platform configurations."""

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._platforms: list[PlatformConfig] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._platforms)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(self._platforms):
            return None

        platform = self._platforms[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return platform.platform_name
        elif role == Qt.ItemDataRole.UserRole:
            return platform.to_dict()

        return None

    def roleNames(self) -> dict[int, bytes]:  # noqa: N802
        return {
            Qt.ItemDataRole.DisplayRole: b"name",
            Qt.ItemDataRole.UserRole: b"platform",
        }

    def set_platforms(self, platforms: list[PlatformConfig]) -> None:
        self.beginResetModel()
        self._platforms = platforms
        self.endResetModel()

    def get_platform(self, index: int) -> PlatformConfig | None:
        if 0 <= index < len(self._platforms):
            return self._platforms[index]
        return None


class PlatformViewModel(QObject):
    """
    ViewModel for platform configuration interface.

    Corresponds to AbstractUI: PlatformConfiguration
    Exposes properties and methods for QML binding.
    """

    # Signals
    loadingChanged = pyqtSignal(bool)  # noqa: N815
    errorChanged = pyqtSignal(str)  # noqa: N815
    platformAdded = pyqtSignal(QVariant)  # noqa: N815
    platformRemoved = pyqtSignal(str)  # noqa: N815
    connectionTested = pyqtSignal(str, bool)  # noqa: N815 (platform_id, success)
    statsChanged = pyqtSignal()  # noqa: N815

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._model = PlatformConfigurationModel()
        self._list_model = PlatformListModel(self)
        self._log = logging.getLogger("edo_client.viewmodel.platform")

    @property
    def list_model(self) -> PlatformListModel:
        """Get the QML-compatible list model."""
        return self._list_model

    # Properties exposed to QML
    @property
    def isLoading(self) -> bool:  # noqa: N802
        return self._model.isLoading

    @isLoading.setter
    def isLoading(self, value: bool):  # noqa: N802
        if self._model.isLoading != value:
            self._model.isLoading = value
            self.loadingChanged.emit(value)

    @property
    def error(self) -> str | None:
        return self._model.error

    @error.setter
    def error(self, value: str | None):
        if self._model.error != value:
            self._model.error = value
            self.errorChanged.emit(value or "")

    @property
    def statistics(self) -> dict[str, Any]:
        """Get platform statistics."""
        return self._model.get_statistics()

    # Filter methods
    @pyqtSlot()
    def toggleEnabledFilter(self):  # noqa: N802
        """Toggle enabled-only filter."""
        self._model.show_only_enabled = not self._model.show_only_enabled
        self._update_list_model()

    @pyqtSlot()
    def toggleConnectedFilter(self):  # noqa: N802
        """Toggle connected-only filter."""
        self._model.show_only_connected = not self._model.show_only_connected
        self._update_list_model()

    @pyqtSlot(str)
    def setDomainFilter(self, domain: str):  # noqa: N802
        """Set domain filter."""
        self._model.domain_filter = domain if domain else None
        self._update_list_model()

    @pyqtSlot(result=QVariant)
    def getAvailableDomains(self) -> Any:  # noqa: N802
        """Get list of available domains."""
        return self._model.get_available_domains()

    # Platform management
    @pyqtSlot(str, str, str)
    def addPlatform(self, platform_id: str, name: str, domain: str = ""):  # noqa: N802
        """Add a new platform configuration."""
        platform = PlatformConfig(
            platform_id=platform_id,
            platform_name=name,
            domain=domain or None,
        )
        self._model.add_platform(platform)
        self._update_list_model()
        self.platformAdded.emit(QVariant(platform.to_dict()))
        self.statsChanged.emit()
        self._log.info("Added platform: %s (%s)", name, platform_id)

    @pyqtSlot(str)
    def removePlatform(self, platform_id: str):  # noqa: N802
        """Remove a platform configuration."""
        if self._model.remove_platform(platform_id):
            self._update_list_model()
            self.platformRemoved.emit(platform_id)
            self.statsChanged.emit()
            self._log.info("Removed platform: %s", platform_id)

    @pyqtSlot(int, result=QVariant)
    def getPlatform(self, index: int) -> Any:  # noqa: N802
        """Get platform by index."""
        platform = self._list_model.get_platform(index)
        return platform.to_dict() if platform else None

    @pyqtSlot(str, result=QVariant)
    def getPlatformById(self, platform_id: str) -> Any:  # noqa: N802
        """Get platform by ID."""
        platform = self._model.get_platform(platform_id)
        return platform.to_dict() if platform else None

    # Connection testing
    @pyqtSlot(str)
    def testConnection(self, platform_id: str):  # noqa: N802
        """Test platform connection."""
        platform = self._model.get_platform(platform_id)
        if platform:
            success = platform.test_connection()
            self.connectionTested.emit(platform_id, success)
            self._update_list_model()
            self._log.info("Connection test for %s: %s",
                            platform_id, "✓" if success else "✗")

    @pyqtSlot()
    def testAllConnections(self):  # noqa: N802
        """Test all platform connections."""
        results = self._model.test_all_connections()
        for platform_id, success in results.items():
            self.connectionTested.emit(platform_id, success)
        self._update_list_model()
        self._log.info("Tested all connections: %d/%d successful",
                        sum(results.values()), len(results))

    # Configuration
    @pyqtSlot(str, str)
    def setApiEndpoint(self, platform_id: str, endpoint: str):  # noqa: N802
        """Set API endpoint for a platform."""
        platform = self._model.get_platform(platform_id)
        if platform:
            platform.api_endpoint = endpoint
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Set API endpoint for %s: %s", platform_id, endpoint)

    @pyqtSlot(str, str)
    def setAuthType(self, platform_id: str, auth_type: str):  # noqa: N802
        """Set authentication type."""
        platform = self._model.get_platform(platform_id)
        if platform:
            platform.auth_type = AuthType(auth_type)
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Set auth type for %s: %s", platform_id, auth_type)

    @pyqtSlot(str, bool)
    def toggleEnabled(self, platform_id: str, enabled: bool):  # noqa: N802
        """Enable/disable a platform."""
        platform = self._model.get_platform(platform_id)
        if platform:
            platform.is_enabled = enabled
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Platform %s %s", platform_id, "enabled" if enabled else "disabled")

    @pyqtSlot(str, str, str, bool)
    def setPublicationDefaults(  # noqa: N802
        self,
        platform_id: str,
        license: str,
        access_type: str,
        auto_publish: bool
    ):  # noqa: N802
        """Set publication defaults."""
        platform = self._model.get_platform(platform_id)
        if platform:
            platform.defaults.default_license = license
            platform.defaults.default_access_type = access_type
            platform.defaults.auto_publish = auto_publish
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Updated publication defaults for %s", platform_id)

    # Schema mapping
    @pyqtSlot(str, str, str)
    def createMapping(  # noqa: N802
        self,
        platform_id: str,
        source_schema: str,
        target_schema: str
    ):  # noqa: N802
        """Create a schema mapping for a platform."""
        platform = self._model.get_platform(platform_id)
        if platform:
            mapping = PlatformMapping(
                mapping_id=f"map_{platform_id}",
                platform_id=platform_id,
                source_schema=source_schema,
                target_schema=target_schema,
            )
            platform.mapping = mapping
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Created mapping for %s: %s → %s",
                            platform_id, source_schema, target_schema)

    @pyqtSlot(str, str, str, str)
    def addFieldMapping(  # noqa: N802
        self,
        platform_id: str,
        source_field: str,
        target_field: str,
        transformation: str = ""
    ):  # noqa: N802
        """Add a field mapping."""
        platform = self._model.get_platform(platform_id)
        if platform and platform.mapping:
            mapping = FieldMapping(
                source_field=source_field,
                target_field=target_field,
                transformation_rule=transformation or None
            )
            platform.mapping.add_mapping(mapping)
            platform.update_timestamp()
            self._update_list_model()
            self._log.info("Added field mapping for %s: %s → %s",
                            platform_id, source_field, target_field)

    @pyqtSlot(str, result=QVariant)
    def getFieldMappings(self, platform_id: str) -> Any:  # noqa: N802
        """Get field mappings for a platform."""
        platform = self._model.get_platform(platform_id)
        if platform and platform.mapping:
            return [
                {
                    "sourceField": m.source_field,
                    "targetField": m.target_field,
                    "transformationRule": m.transformation_rule,
                    "isRequired": m.is_required,
                    "defaultValue": m.default_value
                }
                for m in platform.mapping.field_mappings
            ]
        return []

    # Plugin management
    @pyqtSlot(result=QVariant)
    def getAvailablePlugins(self) -> Any:  # noqa: N802
        """Get list of available plugins."""
        return [p.to_dict() for p in self._model.plugins]

    @pyqtSlot(str)
    def installPlugin(self, plugin_id: str):  # noqa: N802
        """Install a plugin."""
        for plugin in self._model.plugins:
            if plugin.plugin_id == plugin_id:
                plugin.is_installed = True
                plugin.installation_date = datetime.now()
                self._log.info("Installed plugin: %s", plugin_id)
                break

    @pyqtSlot(str)
    def uninstallPlugin(self, plugin_id: str):  # noqa: N802
        """Uninstall a plugin."""
        for plugin in self._model.plugins:
            if plugin.plugin_id == plugin_id:
                plugin.is_installed = False
                plugin.installation_date = None
                self._log.info("Uninstalled plugin: %s", plugin_id)
                break

    # Helper methods
    def _update_list_model(self):
        """Update the QML list model with filtered platforms."""
        filtered = self._model.get_filtered_platforms()
        self._list_model.set_platforms(filtered)

    # Data loading
    def load_platforms(self, platforms: list[dict[str, Any]]) -> None:
        """Load platform configurations from backend response."""
        try:
            configs = []
            for data in platforms:
                config = PlatformConfig(
                    platform_id=data.get("platformId", ""),
                    platform_name=data.get("platformName", ""),
                    domain=data.get("domain"),
                    api_endpoint=data.get("apiEndpoint"),
                    plugin_installed=data.get("pluginInstalled", False),
                    is_enabled=data.get("isEnabled", True),
                    publications_count=data.get("publicationsCount", 0),
                )

                # Parse enums
                if data.get("authType"):
                    config.auth_type = AuthType(data["authType"])
                if data.get("connectionStatus"):
                    config.connection_status = ConnectionStatus(data["connectionStatus"])

                configs.append(config)

            self._model.platforms = configs
            self._update_list_model()
            self.statsChanged.emit()
            self._log.info("Loaded %d platform configurations", len(configs))

        except Exception as e:
            self._log.error("Failed to load platforms: %s", e)
            self.error = f"Failed to load platforms: {e}"

    def refresh(self) -> None:
        """Refresh platform configurations."""
        self._log.info("Refreshing platform configurations...")
        self.isLoading = True
        self.error = None
        # In real implementation, would fetch from backend
        self.isLoading = False
        self.statsChanged.emit()
