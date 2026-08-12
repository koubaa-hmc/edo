"""
Metadata View Model - Abstract Model Trees 3 & 4: CreateMetadataWizard & EditMetadata

ViewModel for PyQt/QML binding following MDUID specification.
Supports CF1, CF2, CF3, CF4 for FAIR Phases: PLAN/COLLECT/PROCESS/PRESERVE
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from PyQt6.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot

from ..models.metadata import (
    FieldDataType,
    MetadataField,
    MetadataModel,
    MetadataSection,
    MetadataTemplate,
)


class WizardStep:
    """Wizard step definitions matching AbstractUI: CreateMetadataWizard."""

    STEP_SELECT_TEMPLATE = 1
    STEP_BASIC_INFORMATION = 2
    STEP_SCIENTIFIC_CONTEXT = 3
    STEP_TECHNICAL_METADATA = 4
    STEP_ACCESS_AND_REUSE = 5
    STEP_TARGET_PLATFORMS = 6

    TITLES = {
        STEP_SELECT_TEMPLATE: "Select Template",
        STEP_BASIC_INFORMATION: "Basic Information",
        STEP_SCIENTIFIC_CONTEXT: "Scientific Context",
        STEP_TECHNICAL_METADATA: "Technical Metadata",
        STEP_ACCESS_AND_REUSE: "Access & Reuse",
        STEP_TARGET_PLATFORMS: "Target Platforms",
    }

    @classmethod
    def get_title(cls, step: int) -> str:
        return cls.TITLES.get(step, f"Step {step}")

    @classmethod
    def get_total_steps(cls) -> int:
        return len(cls.TITLES)


class MetadataViewModel(QObject):
    """
    ViewModel for metadata creation and editing.

    Corresponds to AbstractUI: CreateMetadataWizard & EditMetadata
    Exposes properties and methods for QML binding.
    """

    # Signals
    stepChanged = pyqtSignal(int)  # noqa: N815
    validationChanged = pyqtSignal()  # noqa: N815
    completenessChanged = pyqtSignal(float)  # noqa: N815
    fieldValueChanged = pyqtSignal(str, QVariant)  # noqa: N815
    sectionExpanded = pyqtSignal(str)  # noqa: N815
    recommendationsUpdated = pyqtSignal(QVariant)  # noqa: N815
    autoSaveCompleted = pyqtSignal()  # noqa: N815
    canSubmitChanged = pyqtSignal(bool)  # noqa: N815

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._model = MetadataModel()
        self._log = logging.getLogger("edo_client.viewmodel.metadata")
        self._can_submit = False

    # Properties exposed to QML
    @property
    def currentStep(self) -> int:  # noqa: N802
        return self._model.current_step

    @property
    def totalSteps(self) -> int:  # noqa: N802
        return self._model.total_steps

    @property
    def currentStepTitle(self) -> str:  # noqa: N802
        return WizardStep.get_title(self._model.current_step)

    @property
    def datasetTitle(self) -> str:  # noqa: N802
        return self._model.title

    @property
    def status(self) -> str:  # noqa: N802
        return self._model.status

    @property
    def version(self) -> str:  # noqa: N802
        return self._model.version

    @property
    def completenessScore(self) -> float:  # noqa: N802
        return self._model.completeness_score * 100  # As percentage

    @property
    def hasValidationErrors(self) -> bool:  # noqa: N802
        return self._model.has_validation_errors()

    @property
    def canSubmit(self) -> bool:  # noqa: N802
        return self._can_submit

    @property
    def isDirty(self) -> bool:  # noqa: N802
        """Check if any field has been modified."""
        for section in self._model.sections:
            for field in section.fields:
                if field.is_dirty:
                    return True
        return False

    @property
    def lastSaved(self) -> str | None:  # noqa: N802
        if self._model.last_saved:
            return self._model.last_saved.strftime("%Y-%m-%d %H:%M")
        return None

    # Section access
    @pyqtSlot(result=QVariant)
    def getSections(self) -> Any:  # noqa: N802
        """Get all sections as JSON-serializable dict."""
        return [
            {
                "sectionId": s.section_id,
                "title": s.title,
                "description": s.description,
                "isExpanded": s.is_expanded,
                "completenessScore": s.get_completeness_score() * 100,
                "fields": [f.to_dict() for f in s.fields]
            }
            for s in self._model.sections
        ]

    @pyqtSlot(str, result=QVariant)
    def getSection(self, section_id: str) -> Any:  # noqa: N802
        """Get a specific section by ID."""
        section = self._model.get_section(section_id)
        return section.to_dict() if section else None

    @pyqtSlot(str, str, result=QVariant)
    def getField(self, section_id: str, field_id: str) -> Any:  # noqa: N802
        """Get a specific field."""
        field = self._model.get_field(field_id)
        return field.to_dict() if field else None

    # Navigation
    @pyqtSlot(result=bool)
    def nextStep(self) -> bool:  # noqa: N802
        """Advance to next wizard step."""
        if self._model.next_step():
            self.stepChanged.emit(self._model.current_step)
            self._log.info("Advanced to step %d: %s",
                            self._model.current_step,
                            WizardStep.get_title(self._model.current_step))
            return True
        return False

    @pyqtSlot(result=bool)
    def previousStep(self) -> bool:  # noqa: N802
        """Go back to previous step."""
        if self._model.previous_step():
            self.stepChanged.emit(self._model.current_step)
            return True
        return False

    @pyqtSlot(int, result=bool)
    def goToStep(self, step: int) -> bool:  # noqa: N802
        """Jump to specific step."""
        if 1 <= step <= self._model.total_steps:
            # Validate current step before jumping
            if step > self._model.current_step:
                # Moving forward - validate current step first
                if not self._validate_current_step():
                    return False

            self._model.current_step = step
            self.stepChanged.emit(step)
            return True
        return False

    # Field operations
    @pyqtSlot(str, QVariant)
    def setFieldValue(self, field_id: str, value: Any):  # noqa: N802
        """Set a field value."""
        if self._model.set_field_value(field_id, value):
            self.fieldValueChanged.emit(field_id, QVariant(value))
            self._validate_current_step()
            self._update_can_submit()

            # Auto-save if enabled
            if self._model.auto_save_enabled:
                self._schedule_auto_save()
        else:
            self._log.warning("Field not found: %s", field_id)

    @pyqtSlot(str)
    def toggleSectionExpanded(self, section_id: str):  # noqa: N802
        """Toggle section expanded state."""
        section = self._model.get_section(section_id)
        if section:
            section.is_expanded = not section.is_expanded
            self.sectionExpanded.emit(section_id)

    # Validation
    @pyqtSlot(result=QVariant)
    def validateAll(self) -> Any:  # noqa: N802
        """Validate all fields and return results."""
        errors = self._model.validate_all()
        self.validationChanged.emit()
        self._update_can_submit()

        return {
            "hasErrors": self._model.has_validation_errors(),
            "errorCount": len([e for e in errors if e.is_error()]),
            "warningCount": len([e for e in errors if e.is_warning()]),
            "errors": [
                {"fieldId": e.field_id, "level": e.level.value, "message": e.message}
                for e in errors
            ]
        }

    @pyqtSlot(result=bool)
    def validateCurrentStep(self) -> bool:  # noqa: N802
        """Validate current wizard step."""
        return self._validate_current_step()

    def _validate_current_step(self) -> bool:
        """Validate fields in current step."""
        step_sections = self._model._get_sections_for_step(self._model.current_step)
        has_errors = False

        for section in step_sections:
            errors = section.validate_all()
            if any(e.is_error() for e in errors):
                has_errors = True

        self.validationChanged.emit()
        return not has_errors

    def _update_can_submit(self):
        """Update can_submit flag."""
        new_can_submit = self._model.can_submit()
        if new_can_submit != self._can_submit:
            self._can_submit = new_can_submit
            self.canSubmitChanged.emit(new_can_submit)

    # Recommendations (CF3)
    @pyqtSlot(str)
    def applySuggestion(self, field_id: str):  # noqa: N802
        """Apply a suggestion to a field."""
        field = self._model.get_field(field_id)
        if field and field.suggestions:
            # Apply first suggestion (in real implementation, would be more sophisticated)
            field.value = field.suggestions[0]
            field.is_dirty = True
            self.fieldValueChanged.emit(field_id, QVariant(field.value))
            self._log.info("Applied suggestion to field: %s", field_id)

    @pyqtSlot(result=QVariant)
    def getRecommendations(self) -> Any:  # noqa: N802
        """Get current recommendations."""
        return {
            "completenessScore": self.completenessScore,
            "recommendations": self._model.recommendations,
            "missingFields": self._get_missing_required_fields()
        }

    def _get_missing_required_fields(self) -> list[str]:
        """Get list of missing required fields."""
        missing = []
        for section in self._model.sections:
            for field in section.fields:
                if field.required and (field.value is None or field.value == ""):
                    missing.append(f"{section.title}: {field.display_name}")
        return missing

    # RO-Crate generation (CF3)
    @pyqtSlot(result=QVariant)
    def generateROCrate(self) -> Any:  # noqa: N802
        """Generate RO-Crate JSON-LD representation."""
        crate = self._model.to_ro_crate()
        return crate

    @pyqtSlot(result=str)
    def getROCrateJson(self) -> str:  # noqa: N802
        """Get RO-Crate as JSON string."""
        self._model.to_ro_crate()
        return self._model.ro_crate_json or "{}"

    # Save operations
    @pyqtSlot()
    def saveDraft(self):  # noqa: N802
        """Save current state as draft."""
        self._model.is_draft = True
        self._model.status = "draft"
        self._model.last_saved = datetime.now()
        self._log.info("Draft saved at %s", self._model.last_saved)
        self.autoSaveCompleted.emit()

    @pyqtSlot()
    def submitForReview(self):  # noqa: N802
        """Submit metadata for review."""
        if not self._model.can_submit():
            self._log.warning("Cannot submit: validation failed")
            self.validateAll()
            return

        self._model.is_draft = False
        self._model.status = "under-review"
        self._model.last_saved = datetime.now()
        self._log.info("Submitted for review: %s", self._model.dataset_id or "new")

    def _schedule_auto_save(self):
        """Schedule auto-save (placeholder)."""
        # In real implementation, would use Q-Timer
        pass

    # Template loading
    @pyqtSlot(str)
    def loadTemplate(self, template_id: str):  # noqa: N802
        """Load a metadata template."""
        # In real implementation, would load from template repository
        self._log.info("Loading template: %s", template_id)

        # For demo, create basic template
        template = MetadataTemplate(
            template_id=template_id,
            schema_name="DataCite",
            schema_version="4.4",
            domain="General",
        )

        self._model.template = template
        self._model.total_steps = WizardStep.get_total_steps()

    # Reset
    @pyqtSlot()
    def reset(self):  # noqa: N802
        """Reset model to initial state."""
        self._model.reset()
        self._can_submit = False
        self.stepChanged.emit(1)
        self.completenessChanged.emit(0.0)
        self.canSubmitChanged.emit(False)
        self._log.info("Metadata model reset")

    # Initialize with sample data
    def initialize_sample(self):
        """Initialize with sample sections for testing."""
        # Identification section
        ident_section = MetadataSection(
            section_id="identification",
            title="Identification",
            description="Basic identification information",
        )
        ident_section.add_field(MetadataField(
            field_id="title",
            display_name="Title",
            data_type=FieldDataType.TEXT,
            required=True,
            min_length=10,
            placeholder="Enter a descriptive title"
        ))
        ident_section.add_field(MetadataField(
            field_id="doi",
            display_name="DOI",
            data_type=FieldDataType.TEXT,
            placeholder="10.xxxx/xxxxx",
            help_text="Digital Object Identifier (auto-generated if empty)"
        ))
        self._model.add_section(ident_section)

        # Creators section
        creators_section = MetadataSection(
            section_id="creators",
            title="Creators",
            description="Dataset authors and contributors",
        )
        creators_section.add_field(MetadataField(
            field_id="creators",
            display_name="Creators",
            data_type=FieldDataType.REPEATING_GROUP,
            required=True,
            help_text="Add all contributors with ORCiD where available"
        ))
        self._model.add_section(creators_section)

        self._log.info("Initialized sample metadata structure")
