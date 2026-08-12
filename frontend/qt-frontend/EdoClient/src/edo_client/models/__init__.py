"""
EDO Client - Data Models

This package contains the data models that back the Abstract UI Trees
defined in the MDUID specification.
"""

from .catalog import DatasetCard, CatalogModel
from .metadata import MetadataField, MetadataSection, MetadataModel
from .review import ReviewItem, ReviewQueueModel
from .user import UserProfile, UserRole
from .platform import PlatformConfig, PlatformMapping

__all__ = [
    'DatasetCard',
    'CatalogModel',
    'MetadataField',
    'MetadataSection',
    'MetadataModel',
    'ReviewItem',
    'ReviewQueueModel',
    'UserProfile',
    'UserRole',
    'PlatformConfig',
    'PlatformMapping',
]
