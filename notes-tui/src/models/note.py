"""
Note Model
==========

+------------------+
|      NOTE        |
+------------------+
| PK id: string    |
|    title: string |
|    content: text |
|    created_at    |
|    updated_at    |
| FK notebook_id   |
+------------------+
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Note:
    """Represents a single note in the application."""

    id: str = field(default_factory=lambda: f"note_{uuid.uuid4().hex[:8]}")
    title: str = "Untitled"
    content: str = ""
    notebook_id: str = "default"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_content(self, title: str, content: str) -> None:
        """Update note title and content."""
        self.title = title
        self.content = content
        self.updated_at = datetime.now()

    def move_to_notebook(self, notebook_id: str) -> None:
        """Move note to a different notebook."""
        self.notebook_id = notebook_id
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert note to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "notebook_id": self.notebook_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """Create a Note from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            notebook_id=data.get("notebook_id", "default"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def matches_search(self, query: str) -> bool:
        """Check if note matches a search query."""
        query_lower = query.lower()
        return (
            query_lower in self.title.lower() or
            query_lower in self.content.lower()
        )

    def get_preview(self, max_length: int = 50) -> str:
        """Get a preview of the note content."""
        content = self.content.replace("\n", " ").strip()
        if len(content) > max_length:
            return content[:max_length - 3] + "..."
        return content

    def __str__(self) -> str:
        return f"Note({self.id}: {self.title})"
