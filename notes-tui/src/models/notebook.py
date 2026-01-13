"""
Notebook Model
==============

+------------------+
|    NOTEBOOK      |
+------------------+
| PK id: string    |
|    name: string  |
|    created_at    |
|    updated_at    |
+------------------+
"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Notebook:
    """Represents a notebook that contains notes."""

    id: str = field(default_factory=lambda: f"nb_{uuid.uuid4().hex[:8]}")
    name: str = "Untitled Notebook"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def rename(self, new_name: str) -> None:
        """Rename the notebook."""
        self.name = new_name
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert notebook to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Notebook":
        """Create a Notebook from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    @classmethod
    def create_default(cls) -> "Notebook":
        """Create the default notebook."""
        return cls(id="default", name="Default")

    def __str__(self) -> str:
        return f"Notebook({self.id}: {self.name})"
