"""
Repository - Data Persistence Layer
====================================

Storage Schema:
+------------------------------------------------------------------+
|                         DATA LAYER                                |
|                                                                   |
|  +------------------+  +------------------+                       |
|  |   NoteRepository |  |   Storage (JSON) |                       |
|  +------------------+  +------------------+                       |
+------------------------------------------------------------------+

JSON File Structure:
{
  "notebooks": [...],
  "notes": [...]
}
"""

import json
import os
from pathlib import Path
from typing import List, Optional

from ..models import Note, Notebook


class Repository:
    """Handles data persistence using JSON file storage."""

    def __init__(self, data_path: Optional[str] = None):
        """Initialize repository with data file path."""
        if data_path is None:
            # Default to data/notes.json relative to project root
            project_root = Path(__file__).parent.parent.parent
            data_path = project_root / "data" / "notes.json"

        self.data_path = Path(data_path)
        self._ensure_data_file()
        self._notes: List[Note] = []
        self._notebooks: List[Notebook] = []
        self.load()

    def _ensure_data_file(self) -> None:
        """Ensure data directory and file exist."""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            self._save_data({"notebooks": [], "notes": []})

    def _load_data(self) -> dict:
        """Load raw data from JSON file."""
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"notebooks": [], "notes": []}

    def _save_data(self, data: dict) -> None:
        """Save raw data to JSON file."""
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self) -> None:
        """Load all data from storage."""
        data = self._load_data()

        # Load notebooks
        self._notebooks = [
            Notebook.from_dict(nb) for nb in data.get("notebooks", [])
        ]

        # Ensure default notebook exists
        if not any(nb.id == "default" for nb in self._notebooks):
            self._notebooks.insert(0, Notebook.create_default())

        # Load notes
        self._notes = [
            Note.from_dict(note) for note in data.get("notes", [])
        ]

    def save(self) -> None:
        """Save all data to storage."""
        data = {
            "notebooks": [nb.to_dict() for nb in self._notebooks],
            "notes": [note.to_dict() for note in self._notes],
        }
        self._save_data(data)

    # ==================== Notebook Operations ====================

    def get_all_notebooks(self) -> List[Notebook]:
        """Get all notebooks."""
        return self._notebooks.copy()

    def get_notebook(self, notebook_id: str) -> Optional[Notebook]:
        """Get a notebook by ID."""
        for nb in self._notebooks:
            if nb.id == notebook_id:
                return nb
        return None

    def create_notebook(self, name: str) -> Notebook:
        """Create a new notebook."""
        notebook = Notebook(name=name)
        self._notebooks.append(notebook)
        self.save()
        return notebook

    def update_notebook(self, notebook: Notebook) -> None:
        """Update an existing notebook."""
        for i, nb in enumerate(self._notebooks):
            if nb.id == notebook.id:
                self._notebooks[i] = notebook
                self.save()
                return

    def delete_notebook(self, notebook_id: str) -> bool:
        """Delete a notebook (moves notes to default)."""
        if notebook_id == "default":
            return False  # Cannot delete default notebook

        # Move notes to default notebook
        for note in self._notes:
            if note.notebook_id == notebook_id:
                note.move_to_notebook("default")

        # Remove notebook
        self._notebooks = [nb for nb in self._notebooks if nb.id != notebook_id]
        self.save()
        return True

    def get_note_count_for_notebook(self, notebook_id: str) -> int:
        """Get the number of notes in a notebook."""
        return sum(1 for note in self._notes if note.notebook_id == notebook_id)

    # ==================== Note Operations ====================

    def get_all_notes(self) -> List[Note]:
        """Get all notes."""
        return sorted(self._notes, key=lambda n: n.updated_at, reverse=True)

    def get_notes_by_notebook(self, notebook_id: str) -> List[Note]:
        """Get all notes in a specific notebook."""
        notes = [n for n in self._notes if n.notebook_id == notebook_id]
        return sorted(notes, key=lambda n: n.updated_at, reverse=True)

    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID."""
        for note in self._notes:
            if note.id == note_id:
                return note
        return None

    def create_note(self, title: str = "Untitled", content: str = "",
                    notebook_id: str = "default") -> Note:
        """Create a new note."""
        note = Note(title=title, content=content, notebook_id=notebook_id)
        self._notes.append(note)
        self.save()
        return note

    def update_note(self, note: Note) -> None:
        """Update an existing note."""
        for i, n in enumerate(self._notes):
            if n.id == note.id:
                self._notes[i] = note
                self.save()
                return

    def delete_note(self, note_id: str) -> bool:
        """Delete a note."""
        original_count = len(self._notes)
        self._notes = [n for n in self._notes if n.id != note_id]
        if len(self._notes) < original_count:
            self.save()
            return True
        return False

    def search_notes(self, query: str) -> List[Note]:
        """Search notes by title and content."""
        if not query:
            return []
        results = [note for note in self._notes if note.matches_search(query)]
        return sorted(results, key=lambda n: n.updated_at, reverse=True)
