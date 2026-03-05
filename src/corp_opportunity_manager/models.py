"""Data models for opportunity management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass
class OpportunityConfig:
    """User input for creating a new opportunity."""

    client: str
    product: str
    contact: str = ""
    stage: str = "discovery"
    topic: str = "Discovery"
    date: date = field(default_factory=date.today)


@dataclass
class ProjectInfo:
    """Metadata about a created project, persisted to project-info.yaml."""

    client: str
    product: str
    contact: str
    stage: str
    created: str
    folder_name: str
    folder_path: str

    def to_yaml_dict(self) -> dict:
        """Return dict suitable for YAML serialization."""
        return {
            "client": self.client,
            "product": self.product,
            "contact": self.contact,
            "stage": self.stage,
            "created": self.created,
            "folder_name": self.folder_name,
        }


@dataclass
class CreationResult:
    """Summary of everything created by `com new`."""

    project_info: ProjectInfo
    folder_path: Path
    deck_path: Path | None
    info_path: Path
    notes_path: Path
