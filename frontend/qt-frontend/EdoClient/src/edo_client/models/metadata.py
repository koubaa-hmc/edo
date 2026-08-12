"""
Metadata Models - Abstract Model Trees 3 & 4: CreateMetadataWizard & EditMetadata

Supports CF1, CF2, CF3, CF4 for FAIR Phases: PLAN/COLLECT/PROCESS/PRESERVE
Primary Roles: research_fellow, data_steward
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum


class FieldDataType(Enum):
    """Data types for metadata fields."""
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    URL = "url"
    EMAIL = "email"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTISELECT = "multiselect"
    TAGS = "tags"
    FILE = "file"
    REPEATING_GROUP = "repeating_group"


class ValidationLevel(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationResult:
    """Result of validating a metadata field or section."""
    field_id: str
    level: ValidationLevel
    message: str
    suggestion: Optional[str] = None
    
    def is_error(self) -> bool:
        return self.level == ValidationLevel.ERROR
    
    def is_warning(self) -> bool:
        return self.level == ValidationLevel.WARNING


@dataclass
class VocabularyTerm:
    """Controlled vocabulary term."""
    term_id: str
    label: str
    definition: Optional[str] = None
    uri: Optional[str] = None
    broader_term: Optional[str] = None
    narrower_terms: List[str] = field(default_factory=list)


@dataclass
class MetadataField:
    """
    Represents a single metadata field in the editor.
    
    Corresponds to AbstractUI: EditMetadata → LeftPanel → DynamicFormFields
    """
    field_id: str
    display_name: str
    description: Optional[str] = None
    data_type: FieldDataType = FieldDataType.TEXT
    required: bool = False
    repeatable: bool = False
    value: Any = None
    default_value: Any = None
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    
    # Validation
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None  # Regex pattern
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    
    # Controlled vocabulary
    vocabulary: Optional[List[VocabularyTerm]] = None
    vocabulary_uri: Optional[str] = None
    
    # Recommendations (CF3)
    suggestions: List[Any] = field(default_factory=list)
    
    # State
    is_dirty: bool = False
    validation_errors: List[ValidationResult] = field(default_factory=list)
    
    def validate(self) -> List[ValidationResult]:
        """Validate field value against constraints."""
        errors = []
        
        # Required check
        if self.required and (self.value is None or self.value == ""):
            errors.append(ValidationResult(
                field_id=self.field_id,
                level=ValidationLevel.ERROR,
                message=f"{self.display_name} is required"
            ))
            return errors
        
        # Skip further validation if empty and not required
        if self.value is None or self.value == "":
            return errors
        
        # String length checks
        if isinstance(self.value, str):
            if self.min_length and len(self.value) < self.min_length:
                errors.append(ValidationResult(
                    field_id=self.field_id,
                    level=ValidationLevel.ERROR,
                    message=f"{self.display_name} must be at least {self.min_length} characters"
                ))
            if self.max_length and len(self.value) > self.max_length:
                errors.append(ValidationResult(
                    field_id=self.field_id,
                    level=ValidationLevel.ERROR,
                    message=f"{self.display_name} cannot exceed {self.max_length} characters"
                ))
        
        # Pattern matching
        if self.pattern and isinstance(self.value, str):
            import re
            if not re.match(self.pattern, self.value):
                errors.append(ValidationResult(
                    field_id=self.field_id,
                    level=ValidationLevel.ERROR,
                    message=f"{self.display_name} format is invalid"
                ))
        
        # Numeric range checks
        if isinstance(self.value, (int, float)):
            if self.min_value is not None and self.value < self.min_value:
                errors.append(ValidationResult(
                    field_id=self.field_id,
                    level=ValidationLevel.ERROR,
                    message=f"{self.display_name} must be at least {self.min_value}"
                ))
            if self.max_value is not None and self.value > self.max_value:
                errors.append(ValidationResult(
                    field_id=self.field_id,
                    level=ValidationLevel.ERROR,
                    message=f"{self.display_name} cannot exceed {self.max_value}"
                ))
        
        self.validation_errors = errors
        return errors
    
    def reset(self) -> None:
        """Reset field to default state."""
        self.value = self.default_value
        self.is_dirty = False
        self.validation_errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "fieldId": self.field_id,
            "displayName": self.display_name,
            "description": self.description,
            "dataType": self.data_type.value,
            "required": self.required,
            "repeatable": self.repeatable,
            "value": self.value,
            "placeholder": self.placeholder,
            "helpText": self.help_text,
            "vocabulary": [
                {"termId": t.term_id, "label": t.label, "uri": t.uri}
                for t in self.vocabulary
            ] if self.vocabulary else None,
            "suggestions": self.suggestions,
            "validationErrors": [
                {"level": e.level.value, "message": e.message}
                for e in self.validation_errors
            ]
        }


@dataclass
class MetadataSection:
    """
    Groups related metadata fields.
    
    Corresponds to AbstractUI: EditMetadata → LeftPanel → SectionTabs
    """
    section_id: str
    title: str
    description: Optional[str] = None
    fields: List[MetadataField] = field(default_factory=list)
    icon: Optional[str] = None
    is_expanded: bool = True
    
    def add_field(self, field: MetadataField) -> None:
        """Add a field to this section."""
        self.fields.append(field)
    
    def get_field(self, field_id: str) -> Optional[MetadataField]:
        """Get a specific field by ID."""
        for f in self.fields:
            if f.field_id == field_id:
                return f
        return None
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all fields in section."""
        errors = []
        for field in self.fields:
            errors.extend(field.validate())
        return errors
    
    def get_completeness_score(self) -> float:
        """Calculate completion percentage (0.0 to 1.0)."""
        if not self.fields:
            return 1.0
        
        required_fields = [f for f in self.fields if f.required]
        if not required_fields:
            return 1.0
        
        filled_count = sum(
            1 for f in required_fields 
            if f.value is not None and f.value != ""
        )
        return filled_count / len(required_fields)


@dataclass
class MetadataTemplate:
    """
    Metadata schema template.
    
    Corresponds to AbstractUI: CreateMetadataWizard → Step1: SelectTemplate
    """
    template_id: str
    schema_name: str
    schema_version: str
    domain: Optional[str] = None
    description: Optional[str] = None
    sections: List[MetadataSection] = field(default_factory=list)
    field_count: int = 0
    is_custom: bool = False
    
    def __post_init__(self):
        self.field_count = sum(len(s.fields) for s in self.sections)
    
    def get_all_fields(self) -> List[MetadataField]:
        """Get flattened list of all fields."""
        fields = []
        for section in self.sections:
            fields.extend(section.fields)
        return fields
    
    def get_required_fields(self) -> List[MetadataField]:
        """Get all required fields."""
        return [f for f in self.get_all_fields() if f.required]


@dataclass
class MetadataModel:
    """
    Complete metadata model for creation/editing.
    
    Corresponds to AbstractUI: CreateMetadataWizard & EditMetadata
    """
    dataset_id: Optional[str] = None
    title: str = ""
    template: Optional[MetadataTemplate] = None
    sections: List[MetadataSection] = field(default_factory=list)
    
    # Wizard state
    current_step: int = 1
    total_steps: int = 6
    is_draft: bool = True
    status: str = "draft"  # draft | published | under-review
    
    # Versioning
    version: str = "1.0"
    previous_versions: List[str] = field(default_factory=list)
    
    # Validation & recommendations
    validation_results: List[ValidationResult] = field(default_factory=list)
    completeness_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
    # RO-Crate preview (CF3)
    ro_crate_json: Optional[str] = None
    
    # Change tracking
    change_history: List[Dict[str, Any]] = field(default_factory=list)
    auto_save_enabled: bool = True
    last_saved: Optional[datetime] = None
    
    def add_section(self, section: MetadataSection) -> None:
        """Add a section to the model."""
        self.sections.append(section)
    
    def get_section(self, section_id: str) -> Optional[MetadataSection]:
        """Get a specific section by ID."""
        for s in self.sections:
            if s.section_id == section_id:
                return s
        return None
    
    def get_field(self, field_id: str) -> Optional[MetadataField]:
        """Get a field across all sections."""
        for section in self.sections:
            field = section.get_field(field_id)
            if field:
                return field
        return None
    
    def set_field_value(self, field_id: str, value: Any) -> bool:
        """Set a field value. Returns True if field found."""
        field = self.get_field(field_id)
        if field:
            field.value = value
            field.is_dirty = True
            return True
        return False
    
    def validate_all(self) -> List[ValidationResult]:
        """Validate all sections and fields."""
        errors = []
        for section in self.sections:
            errors.extend(section.validate_all())
        self.validation_results = errors
        return errors
    
    def calculate_completeness(self) -> float:
        """Calculate overall completeness score."""
        if not self.sections:
            return 0.0
        
        scores = [s.get_completeness_score() for s in self.sections]
        self.completeness_score = sum(scores) / len(scores)
        return self.completeness_score
    
    def has_validation_errors(self) -> bool:
        """Check if there are any validation errors."""
        return any(e.is_error() for e in self.validation_results)
    
    def can_submit(self) -> bool:
        """Check if metadata can be submitted/published."""
        self.validate_all()
        self.calculate_completeness()
        return not self.has_validation_errors() and self.completeness_score >= 0.8
    
    def to_ro_crate(self) -> Dict[str, Any]:
        """Generate RO-Crate JSON-LD representation."""
        # Simplified RO-Crate structure
        crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@id": "ro-crate-metadata.json",
                    "@type": "CreativeWork",
                    "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}
                },
                {
                    "@id": "./",
                    "@type": "Dataset",
                    "name": self.title,
                    "datePublished": datetime.now().isoformat(),
                }
            ]
        }
        
        # Add creators
        creators = []
        creator_field = self.get_field("creators")
        if creator_field and creator_field.value:
            for creator in creator_field.value:
                creators.append({
                    "@id": f"#creator-{hash(str(creator))}",
                    "@type": "Person",
                    "name": creator.get("name", ""),
                    "identifier": creator.get("orcid")
                })
            crate["@graph"].extend(creators)
            crate["@graph"][1]["creator"] = [
                {"@id": c["@id"]} for c in creators
            ]
        
        self.ro_crate_json = str(crate)
        return crate
    
    def next_step(self) -> bool:
        """Advance wizard step. Returns True if successful."""
        if self.current_step < self.total_steps:
            # Validate current step before advancing
            step_sections = self._get_sections_for_step(self.current_step)
            can_advance = all(
                not any(e.is_error() for e in s.validate_all())
                for s in step_sections
            )
            if can_advance:
                self.current_step += 1
                return True
            return False
        return False
    
    def previous_step(self) -> bool:
        """Go back a wizard step. Returns True if successful."""
        if self.current_step > 1:
            self.current_step -= 1
            return True
        return False
    
    def _get_sections_for_step(self, step: int) -> List[MetadataSection]:
        """Get sections relevant to a wizard step."""
        step_mapping = {
            1: [],  # Template selection
            2: ["identification", "creators", "descriptions"],
            3: ["scientific_context"],
            4: ["technical_metadata"],
            5: ["access_and_reuse"],
            6: ["target_platforms"],
        }
        section_ids = step_mapping.get(step, [])
        return [s for s in self.sections if s.section_id in section_ids]
    
    def reset(self) -> None:
        """Reset model to initial state."""
        self.current_step = 1
        self.is_draft = True
        self.status = "draft"
        self.validation_results = []
        self.completeness_score = 0.0
        self.recommendations = []
        self.change_history = []
        self.last_saved = None
        for section in self.sections:
            for field in section.fields:
                field.reset()
