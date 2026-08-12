"""
EDO Client - View Models

View models bridge data models with UI components (PyQt/QML).
Following MDUID Abstract Model Trees specification.
"""

from .catalog_vm import CatalogViewModel
from .dataset_detail_vm import DatasetDetailViewModel
from .metadata_vm import MetadataViewModel, WizardStep
from .platform_vm import PlatformViewModel
from .review_vm import ReviewViewModel

__all__ = [
    'CatalogViewModel',
    'MetadataViewModel',
    'WizardStep',
    'ReviewViewModel',
    'PlatformViewModel',
    'DatasetDetailViewModel',
]
