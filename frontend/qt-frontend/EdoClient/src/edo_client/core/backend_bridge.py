"""Backend Bridge - Decoupled communication with backend services."""

from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum


class ActionResultStatus(Enum):
    """Status of an action execution result."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


@dataclass
class ActionResult:
    """Result from executing a backend action."""
    
    action_id: str
    status: ActionResultStatus
    data: Any = None
    error: Optional[str] = None
    message: str = ""
    
    @property
    def is_success(self) -> bool:
        return self.status == ActionResultStatus.SUCCESS
    
    @classmethod
    def success(cls, action_id: str, data: Any = None, message: str = "") -> "ActionResult":
        return cls(
            action_id=action_id,
            status=ActionResultStatus.SUCCESS,
            data=data,
            message=message
        )
    
    @classmethod
    def error(cls, action_id: str, error: str, message: str = "") -> "ActionResult":
        return cls(
            action_id=action_id,
            status=ActionResultStatus.ERROR,
            error=error,
            message=message
        )


@dataclass
class ActionSpec:
    """Specification for a backend action."""
    
    action_id: str
    display_name: str
    description: str
    parameters: Dict[str, str] = field(default_factory=dict)
    requires_async: bool = True


class BackendBridge:
    """Bridge between UI and backend services."""
    
    def __init__(self) -> None:
        self._actions: Dict[str, ActionSpec] = {}
        self._handlers: Dict[str, Callable] = {}
        self._setup_builtin_actions()
    
    def _setup_builtin_actions(self) -> None:
        """Register built-in actions."""
        
        # Workspace actions
        self.register_action(ActionSpec(
            action_id="workspace.new",
            display_name="New Workspace",
            description="Create a new workspace",
            parameters={}
        ))
        
        # Edit actions
        self.register_action(ActionSpec(
            action_id="edit.undo",
            display_name="Undo",
            description="Undo last action",
            parameters={}
        ))
        
        # Data actions
        self.register_action(ActionSpec(
            action_id="data.import",
            display_name="Import Dataset",
            description="Import a dataset into the workspace",
            parameters={"path": "Path to dataset file"}
        ))
        
        self.register_action(ActionSpec(
            action_id="data.validate",
            display_name="Validate Data",
            description="Validate selected data",
            parameters={}
        ))
        
        # Ingestion actions (OEP)
        self.register_action(ActionSpec(
            action_id="ingestion.oep.get_metadata",
            display_name="Get OEP Metadata",
            description="Fetch metadata from Open Energy Platform",
            parameters={"table_name": "Table name on OEP"}
        ))
        
        self.register_action(ActionSpec(
            action_id="ingestion.oep.fetch",
            display_name="Fetch OEP Data",
            description="Fetch data from Open Energy Platform",
            parameters={}
        ))
        
        self.register_action(ActionSpec(
            action_id="ingestion.oep.preprocess",
            display_name="Preprocess Data",
            description="Preprocess fetched data",
            parameters={}
        ))
        
        self.register_action(ActionSpec(
            action_id="ingestion.oep.merge",
            display_name="Merge into Graph",
            description="Merge preprocessed data into knowledge graph",
            parameters={}
        ))
        
        # Ingestion actions (HKG)
        self.register_action(ActionSpec(
            action_id="ingestion.hkg.run",
            display_name="Run HKG Ingestion",
            description="Run Helmholtz KG ingestion workflow",
            parameters={}
        ))
        
        self.register_action(ActionSpec(
            action_id="ingestion.workflow.status",
            display_name="Workflow Status",
            description="Check ingestion workflow status",
            parameters={}
        ))
        
        # Semantic actions
        self.register_action(ActionSpec(
            action_id="semantic.expand",
            display_name="Expand Semantics",
            description="Expand semantic annotations",
            parameters={}
        ))
        
        self.register_action(ActionSpec(
            action_id="semantic.annotate",
            display_name="Annotate Resources",
            description="Annotate resources with ontology terms",
            parameters={}
        ))
        
        # Help actions
        self.register_action(ActionSpec(
            action_id="help.about",
            display_name="About",
            description="Show about dialog",
            parameters={}
        ))
        
        # Navigation actions (no-op for now)
        self.register_action(ActionSpec(
            action_id="nav.datasets",
            display_name="Navigate to Datasets",
            description="Switch to datasets view",
            parameters={}
        ))
        self.register_action(ActionSpec(
            action_id="nav.timeseries",
            display_name="Navigate to Timeseries",
            description="Switch to timeseries view",
            parameters={}
        ))
        self.register_action(ActionSpec(
            action_id="nav.rdf",
            display_name="Navigate to RDF Graph",
            description="Switch to RDF graph view",
            parameters={}
        ))
        self.register_action(ActionSpec(
            action_id="nav.settings",
            display_name="Navigate to Settings",
            description="Switch to settings view",
            parameters={}
        ))
        
        # Register demo handlers for testing
        self._register_demo_handlers()
    
    def _register_demo_handlers(self) -> None:
        """Register demo handlers for UI testing."""
        
        # Navigation handlers (no-op)
        async def demo_nav(params: Dict[str, Any]) -> ActionResult:
            return ActionResult.success(
                params.get("action_id", "nav"),
                message="Navigation updated"
            )
        
        self.register_handler("nav.datasets", demo_nav)
        self.register_handler("nav.timeseries", demo_nav)
        self.register_handler("nav.rdf", demo_nav)
        self.register_handler("nav.settings", demo_nav)
        
        async def demo_import(params: Dict[str, Any]) -> ActionResult:
            await asyncio.sleep(0.5)  # Simulate work
            return ActionResult.success(
                "data.import",
                data={
                    "title": "Demo Dataset",
                    "description": "This is a demo dataset imported for testing",
                    "resources": [{"name": "demo.csv", "format": "CSV"}]
                },
                message="Dataset imported successfully"
            )
        
        async def demo_validate(params: Dict[str, Any]) -> ActionResult:
            await asyncio.sleep(0.3)
            return ActionResult.success(
                "data.validate",
                data={"valid": True, "issues": []},
                message="Validation completed: No issues found"
            )
        
        async def demo_oep_metadata(params: Dict[str, Any]) -> ActionResult:
            await asyncio.sleep(0.5)
            table_name = params.get("table_name", "unknown")
            return ActionResult.success(
                "ingestion.oep.get_metadata",
                data={
                    "table": table_name,
                    "columns": ["timestamp", "value", "unit"],
                    "row_count": 8760
                },
                message=f"Metadata fetched for {table_name}"
            )
        
        async def demo_semantic_expand(params: Dict[str, Any]) -> ActionResult:
            await asyncio.sleep(0.4)
            return ActionResult.success(
                "semantic.expand",
                data={
                    "uri": "https://openenergyontology.org/resource/EnergyPlant_001",
                    "@type": "oeo:EnergyPlant",
                    "rdfs:label": "Solar Park Brandenburg"
                },
                message="Semantic expansion completed"
            )
        
        self.register_handler("data.import", demo_import)
        self.register_handler("data.validate", demo_validate)
        self.register_handler("ingestion.oep.get_metadata", demo_oep_metadata)
        self.register_handler("semantic.expand", demo_semantic_expand)
    
    def register_action(self, spec: ActionSpec) -> None:
        """Register an action specification."""
        self._actions[spec.action_id] = spec
    
    def register_handler(self, action_id: str, handler: Callable) -> None:
        """Register a handler for an action."""
        self._handlers[action_id] = handler
    
    def get_action(self, action_id: str) -> Optional[ActionSpec]:
        """Get action specification by ID."""
        return self._actions.get(action_id)
    
    async def execute(self, action_id: str, **params: Any) -> ActionResult:
        """Execute an action asynchronously."""
        import logging
        log = logging.getLogger("edo_client")
        log.info("⚙️ Executing action: %s with params=%r", action_id, params)
        
        spec = self._actions.get(action_id)
        if not spec:
            log.warning("⚠️ Unknown action: %s", action_id)
            return ActionResult.error(action_id, f"Unknown action: {action_id}")
        
        handler = self._handlers.get(action_id)
        if handler:
            try:
                result = await handler(params)
                log.info("✅ Action completed: %s - %s", action_id, result.message)
                return result
            except Exception as e:
                log.error("❌ Action failed: %s - %s", action_id, str(e))
                return ActionResult.error(action_id, str(e))
        
        # Default: return success with no data
        return ActionResult.success(action_id, message=f"Action {action_id} executed (no handler)")
    
    def get_available_actions(self) -> List[ActionSpec]:
        """Get all registered actions."""
        return list(self._actions.values())


# Global bridge instance
_bridge: Optional[BackendBridge] = None


def get_backend_bridge() -> BackendBridge:
    """Get or create the global backend bridge."""
    global _bridge
    if _bridge is None:
        _bridge = BackendBridge()
    return _bridge
