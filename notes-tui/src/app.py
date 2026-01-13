"""
Notes TUI Application
=====================

Main application class that orchestrates all components.

State Machine:
                              +----------+
                              |  INIT    |
                              +----+-----+
                                   |
                                   | load_data()
                                   v
                              +----------+
            +---------------->| LIST     |<----------------+
            |                 | VIEW     |                 |
            |                 +----+-----+                 |
            |                   |  |  |                    |
            |     +-------------+  |  +-------------+      |
            |     |                |                |      |
            |     | 'e'            | '/'            | 'n'  |
            |     v                v                v      |
        +--------+---+      +----------+      +----------+ |
        |  EDITOR    |      |  SEARCH  |      |   NEW    | |
        |  VIEW      |      |  VIEW    |      |   NOTE   | |
        +--------+---+      +----+-----+      +----+-----+ |
            |    |               |                 |       |
            |    | Esc           | Esc             | Esc   |
            |    +---------------+-----------------+-------+
            |
            | ^S (save)
            v
        [Return to LIST VIEW]
"""

from enum import Enum, auto
from typing import Optional, List

from .models import Note, Notebook
from .storage import Repository
from .tui import Screen, Renderer, InputHandler
from .tui.input_handler import Key, KeyEvent


class AppState(Enum):
    """Application state enumeration."""
    LIST = auto()
    EDITOR = auto()
    SEARCH = auto()
    HELP = auto()
    CONFIRM_DELETE = auto()
    INPUT_NOTEBOOK = auto()
    INPUT_NOTE_TITLE = auto()
    QUIT_CONFIRM = auto()


class App:
    """Main application class."""

    def __init__(self, data_path: Optional[str] = None):
        """Initialize the application."""
        self.repo = Repository(data_path)
        self.screen = Screen()
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()

        # Application state
        self.state = AppState.LIST
        self.running = True

        # Selection state
        self.selected_notebook_idx = 0
        self.selected_note_idx = 0
        self.focus_panel = 'notes'  # 'notebooks' or 'notes'

        # Editor state
        self.editing_note: Optional[Note] = None
        self.editor_content: List[str] = []
        self.cursor_line = 0
        self.cursor_col = 0
        self.scroll_offset = 0
        self.editor_modified = False

        # Search state
        self.search_query = ""
        self.search_results: List[Note] = []
        self.search_selected_idx = 0

        # Input dialog state
        self.input_buffer = ""
        self.input_callback = None

        # Status message
        self.status_message = ""

    def run(self) -> None:
        """Run the main application loop."""
        try:
            self.screen.enter_alternate_screen()
            self.screen.enter_raw_mode()
            self.screen.hide_cursor()

            while self.running:
                self._render()
                self._handle_input()

        finally:
            self.screen.show_cursor()
            self.screen.exit_raw_mode()
            self.screen.exit_alternate_screen()

    def _render(self) -> None:
        """Render the current view based on state."""
        if self.state == AppState.LIST:
            self._render_list_view()
        elif self.state == AppState.EDITOR:
            self._render_editor_view()
        elif self.state == AppState.SEARCH:
            self._render_search_view()
        elif self.state == AppState.HELP:
            self._render_list_view()
            self.renderer.render_help()
        elif self.state == AppState.CONFIRM_DELETE:
            self._render_list_view()
            self._render_delete_confirm()
        elif self.state == AppState.INPUT_NOTEBOOK:
            self._render_list_view()
            self.renderer.render_input_dialog("New notebook name", self.input_buffer)
        elif self.state == AppState.INPUT_NOTE_TITLE:
            self._render_list_view()
            self.renderer.render_input_dialog("Note title", self.input_buffer)
        elif self.state == AppState.QUIT_CONFIRM:
            self._render_list_view()
            self.renderer.render_confirm_dialog("Quit application?", "[y/n]")

    def _render_list_view(self) -> None:
        """Render the main list view."""
        notebooks = self.repo.get_all_notebooks()
        current_nb = notebooks[self.selected_notebook_idx] if notebooks else None

        if current_nb:
            notes = self.repo.get_notes_by_notebook(current_nb.id)
        else:
            notes = []

        note_counts = {nb.id: self.repo.get_note_count_for_notebook(nb.id) for nb in notebooks}

        self.renderer.render_main_view(
            notebooks=notebooks,
            notes=notes,
            selected_notebook_idx=self.selected_notebook_idx,
            selected_note_idx=self.selected_note_idx,
            focus_panel=self.focus_panel,
            note_counts=note_counts,
            status_message=self.status_message
        )

    def _render_editor_view(self) -> None:
        """Render the editor view."""
        if self.editing_note:
            # Update note content from editor
            self.editing_note.content = "\n".join(self.editor_content)
            self.renderer.render_editor(
                note=self.editing_note,
                cursor_line=self.cursor_line,
                cursor_col=self.cursor_col,
                scroll_offset=self.scroll_offset,
                modified=self.editor_modified
            )

    def _render_search_view(self) -> None:
        """Render the search view."""
        notebooks = self.repo.get_all_notebooks()
        notebook_names = {nb.id: nb.name for nb in notebooks}

        self.renderer.render_search(
            query=self.search_query,
            results=self.search_results,
            selected_idx=self.search_selected_idx,
            notebook_names=notebook_names
        )

    def _render_delete_confirm(self) -> None:
        """Render delete confirmation dialog."""
        if self.focus_panel == 'notes':
            msg = "Delete this note?"
        else:
            msg = "Delete this notebook?"
        self.renderer.render_confirm_dialog(msg, "[y/n]")

    def _handle_input(self) -> None:
        """Handle keyboard input based on current state."""
        event = self.input_handler.read_key(timeout=0.1)
        if event is None:
            return

        self.status_message = ""  # Clear status on any input

        if self.state == AppState.LIST:
            self._handle_list_input(event)
        elif self.state == AppState.EDITOR:
            self._handle_editor_input(event)
        elif self.state == AppState.SEARCH:
            self._handle_search_input(event)
        elif self.state == AppState.HELP:
            self.state = AppState.LIST  # Any key closes help
        elif self.state == AppState.CONFIRM_DELETE:
            self._handle_delete_confirm_input(event)
        elif self.state == AppState.INPUT_NOTEBOOK:
            self._handle_input_dialog(event, self._create_notebook_callback)
        elif self.state == AppState.INPUT_NOTE_TITLE:
            self._handle_input_dialog(event, self._create_note_callback)
        elif self.state == AppState.QUIT_CONFIRM:
            self._handle_quit_confirm_input(event)

    def _handle_list_input(self, event: KeyEvent) -> None:
        """Handle input in list view."""
        notebooks = self.repo.get_all_notebooks()
        current_nb = notebooks[self.selected_notebook_idx] if notebooks else None
        notes = self.repo.get_notes_by_notebook(current_nb.id) if current_nb else []

        key = event.key
        char = event.char.lower() if event.key == Key.CHAR else ""

        # Navigation
        if key == Key.DOWN or char == 'j':
            if self.focus_panel == 'notebooks':
                self.selected_notebook_idx = min(self.selected_notebook_idx + 1, len(notebooks) - 1)
                self.selected_note_idx = 0
            else:
                self.selected_note_idx = min(self.selected_note_idx + 1, max(0, len(notes) - 1))

        elif key == Key.UP or char == 'k':
            if self.focus_panel == 'notebooks':
                self.selected_notebook_idx = max(self.selected_notebook_idx - 1, 0)
                self.selected_note_idx = 0
            else:
                self.selected_note_idx = max(self.selected_note_idx - 1, 0)

        elif key == Key.LEFT or char == 'h':
            self.focus_panel = 'notebooks'

        elif key == Key.RIGHT or char == 'l':
            self.focus_panel = 'notes'

        elif key == Key.TAB:
            self.focus_panel = 'notes' if self.focus_panel == 'notebooks' else 'notebooks'

        # Actions
        elif char == 'n':
            self.input_buffer = ""
            self.state = AppState.INPUT_NOTE_TITLE

        elif event.char == 'N':  # Capital N for new notebook
            self.input_buffer = ""
            self.state = AppState.INPUT_NOTEBOOK

        elif char == 'e' or key == Key.ENTER:
            if self.focus_panel == 'notes' and notes:
                self._start_editing(notes[self.selected_note_idx])

        elif char == 'd':
            if self.focus_panel == 'notes' and notes:
                self.state = AppState.CONFIRM_DELETE
            elif self.focus_panel == 'notebooks' and current_nb and current_nb.id != 'default':
                self.state = AppState.CONFIRM_DELETE

        elif char == '/':
            self.search_query = ""
            self.search_results = []
            self.search_selected_idx = 0
            self.state = AppState.SEARCH

        elif char == '?':
            self.state = AppState.HELP

        elif char == 'q' or key == Key.CTRL_Q:
            self.state = AppState.QUIT_CONFIRM

        elif key == Key.CTRL_C:
            self.running = False

    def _handle_editor_input(self, event: KeyEvent) -> None:
        """Handle input in editor view."""
        key = event.key

        if key == Key.ESCAPE:
            if self.editor_modified:
                # Auto-save on exit
                self._save_note()
            self.state = AppState.LIST
            self.screen.hide_cursor()
            return

        if key == Key.CTRL_S:
            self._save_note()
            return

        # Text editing
        if event.is_printable:
            self._insert_char(event.char)
        elif key == Key.ENTER:
            self._insert_newline()
        elif key == Key.BACKSPACE:
            self._delete_char_before()
        elif key == Key.DELETE:
            self._delete_char_at()
        elif key == Key.UP:
            self._move_cursor_up()
        elif key == Key.DOWN:
            self._move_cursor_down()
        elif key == Key.LEFT:
            self._move_cursor_left()
        elif key == Key.RIGHT:
            self._move_cursor_right()
        elif key == Key.HOME:
            self.cursor_col = 0
        elif key == Key.END:
            self.cursor_col = len(self.editor_content[self.cursor_line])

    def _handle_search_input(self, event: KeyEvent) -> None:
        """Handle input in search view."""
        key = event.key

        if key == Key.ESCAPE:
            self.state = AppState.LIST
            return

        if key == Key.ENTER:
            if self.search_results:
                # Open selected note
                note = self.search_results[self.search_selected_idx]
                self._start_editing(note)
            return

        if key == Key.DOWN or key == Key.TAB:
            if self.search_results:
                self.search_selected_idx = (self.search_selected_idx + 1) % len(self.search_results)
            return

        if key == Key.UP:
            if self.search_results:
                self.search_selected_idx = (self.search_selected_idx - 1) % len(self.search_results)
            return

        if event.is_printable:
            self.search_query += event.char
            self._update_search()
        elif key == Key.BACKSPACE and self.search_query:
            self.search_query = self.search_query[:-1]
            self._update_search()

    def _handle_delete_confirm_input(self, event: KeyEvent) -> None:
        """Handle delete confirmation input."""
        char = event.char.lower() if event.key == Key.CHAR else ""

        if char == 'y':
            if self.focus_panel == 'notes':
                notebooks = self.repo.get_all_notebooks()
                current_nb = notebooks[self.selected_notebook_idx]
                notes = self.repo.get_notes_by_notebook(current_nb.id)
                if notes:
                    self.repo.delete_note(notes[self.selected_note_idx].id)
                    self.selected_note_idx = max(0, self.selected_note_idx - 1)
                    self.status_message = "Note deleted"
            else:
                notebooks = self.repo.get_all_notebooks()
                if notebooks[self.selected_notebook_idx].id != 'default':
                    self.repo.delete_notebook(notebooks[self.selected_notebook_idx].id)
                    self.selected_notebook_idx = 0
                    self.status_message = "Notebook deleted"
            self.state = AppState.LIST

        elif char == 'n' or event.key == Key.ESCAPE:
            self.state = AppState.LIST

    def _handle_quit_confirm_input(self, event: KeyEvent) -> None:
        """Handle quit confirmation input."""
        char = event.char.lower() if event.key == Key.CHAR else ""

        if char == 'y':
            self.running = False
        elif char == 'n' or event.key == Key.ESCAPE:
            self.state = AppState.LIST

    def _handle_input_dialog(self, event: KeyEvent, callback) -> None:
        """Handle input dialog."""
        key = event.key

        if key == Key.ESCAPE:
            self.input_buffer = ""
            self.state = AppState.LIST
            self.screen.hide_cursor()
            return

        if key == Key.ENTER:
            if self.input_buffer:
                callback(self.input_buffer)
            self.input_buffer = ""
            self.state = AppState.LIST
            self.screen.hide_cursor()
            return

        if event.is_printable:
            self.input_buffer += event.char
        elif key == Key.BACKSPACE and self.input_buffer:
            self.input_buffer = self.input_buffer[:-1]

    def _create_notebook_callback(self, name: str) -> None:
        """Callback for creating a new notebook."""
        self.repo.create_notebook(name)
        self.status_message = f"Created notebook: {name}"

    def _create_note_callback(self, title: str) -> None:
        """Callback for creating a new note."""
        notebooks = self.repo.get_all_notebooks()
        current_nb = notebooks[self.selected_notebook_idx]
        note = self.repo.create_note(title=title, notebook_id=current_nb.id)
        self._start_editing(note)

    def _start_editing(self, note: Note) -> None:
        """Start editing a note."""
        self.editing_note = note
        self.editor_content = note.content.split("\n") if note.content else [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.scroll_offset = 0
        self.editor_modified = False
        self.state = AppState.EDITOR

    def _save_note(self) -> None:
        """Save the current note."""
        if self.editing_note:
            content = "\n".join(self.editor_content)
            self.editing_note.update_content(self.editing_note.title, content)
            self.repo.update_note(self.editing_note)
            self.editor_modified = False
            self.status_message = "Note saved"

    def _update_search(self) -> None:
        """Update search results."""
        self.search_results = self.repo.search_notes(self.search_query)
        self.search_selected_idx = 0

    # Editor helper methods
    def _insert_char(self, char: str) -> None:
        """Insert a character at cursor position."""
        line = self.editor_content[self.cursor_line]
        self.editor_content[self.cursor_line] = line[:self.cursor_col] + char + line[self.cursor_col:]
        self.cursor_col += 1
        self.editor_modified = True

    def _insert_newline(self) -> None:
        """Insert a newline at cursor position."""
        line = self.editor_content[self.cursor_line]
        before = line[:self.cursor_col]
        after = line[self.cursor_col:]
        self.editor_content[self.cursor_line] = before
        self.editor_content.insert(self.cursor_line + 1, after)
        self.cursor_line += 1
        self.cursor_col = 0
        self.editor_modified = True
        self._adjust_scroll()

    def _delete_char_before(self) -> None:
        """Delete character before cursor (backspace)."""
        if self.cursor_col > 0:
            line = self.editor_content[self.cursor_line]
            self.editor_content[self.cursor_line] = line[:self.cursor_col - 1] + line[self.cursor_col:]
            self.cursor_col -= 1
            self.editor_modified = True
        elif self.cursor_line > 0:
            # Join with previous line
            prev_line = self.editor_content[self.cursor_line - 1]
            curr_line = self.editor_content[self.cursor_line]
            self.editor_content[self.cursor_line - 1] = prev_line + curr_line
            del self.editor_content[self.cursor_line]
            self.cursor_line -= 1
            self.cursor_col = len(prev_line)
            self.editor_modified = True
            self._adjust_scroll()

    def _delete_char_at(self) -> None:
        """Delete character at cursor (delete key)."""
        line = self.editor_content[self.cursor_line]
        if self.cursor_col < len(line):
            self.editor_content[self.cursor_line] = line[:self.cursor_col] + line[self.cursor_col + 1:]
            self.editor_modified = True
        elif self.cursor_line < len(self.editor_content) - 1:
            # Join with next line
            next_line = self.editor_content[self.cursor_line + 1]
            self.editor_content[self.cursor_line] = line + next_line
            del self.editor_content[self.cursor_line + 1]
            self.editor_modified = True

    def _move_cursor_up(self) -> None:
        """Move cursor up one line."""
        if self.cursor_line > 0:
            self.cursor_line -= 1
            self.cursor_col = min(self.cursor_col, len(self.editor_content[self.cursor_line]))
            self._adjust_scroll()

    def _move_cursor_down(self) -> None:
        """Move cursor down one line."""
        if self.cursor_line < len(self.editor_content) - 1:
            self.cursor_line += 1
            self.cursor_col = min(self.cursor_col, len(self.editor_content[self.cursor_line]))
            self._adjust_scroll()

    def _move_cursor_left(self) -> None:
        """Move cursor left one character."""
        if self.cursor_col > 0:
            self.cursor_col -= 1
        elif self.cursor_line > 0:
            self.cursor_line -= 1
            self.cursor_col = len(self.editor_content[self.cursor_line])
            self._adjust_scroll()

    def _move_cursor_right(self) -> None:
        """Move cursor right one character."""
        line = self.editor_content[self.cursor_line]
        if self.cursor_col < len(line):
            self.cursor_col += 1
        elif self.cursor_line < len(self.editor_content) - 1:
            self.cursor_line += 1
            self.cursor_col = 0
            self._adjust_scroll()

    def _adjust_scroll(self) -> None:
        """Adjust scroll offset to keep cursor visible."""
        visible_height = self.screen.height - 8  # Approximate visible content height
        if self.cursor_line < self.scroll_offset:
            self.scroll_offset = self.cursor_line
        elif self.cursor_line >= self.scroll_offset + visible_height:
            self.scroll_offset = self.cursor_line - visible_height + 1
