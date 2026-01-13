"""
Renderer
========

Main rendering engine for the TUI application.

Layout:
+===========================================================================+
|  NOTES TUI                                          [?] Help  [Q] Quit   |
+===========================================================================+
|                          |                                                |
|  NOTEBOOKS               |  NOTES                                         |
|  +-----------------+     |  +---------------------------------------------+
|  | > Default    (5)|     |  | > My First Note              2026-01-14    |
|  |   Work       (3)|     |  |   Shopping List              2026-01-13    |
|  |   Personal   (8)|     |  |   Meeting Notes              2026-01-12    |
|  +-----------------+     |  +---------------------------------------------+
|                          |                                                |
+--------------------------+------------------------------------------------+
|  Status bar                                                               |
+===========================================================================+
"""

from typing import List, Optional, Callable
from datetime import datetime

from .screen import Screen
from ..models import Note, Notebook


class Renderer:
    """Renders the TUI interface."""

    def __init__(self, screen: Screen):
        """Initialize renderer with a screen instance."""
        self.screen = screen

    def render_main_view(
        self,
        notebooks: List[Notebook],
        notes: List[Note],
        selected_notebook_idx: int,
        selected_note_idx: int,
        focus_panel: str,  # 'notebooks' or 'notes'
        note_counts: dict,
        status_message: str = ""
    ) -> None:
        """Render the main list view."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Begin buffered frame (no flicker)
        self.screen.begin_frame()

        # Clear all lines by writing spaces (overwrite old content)
        for y in range(1, h + 1):
            self.screen.write_at(1, y, " " * w)

        # Header
        self._render_header(w)

        # Calculate panel dimensions
        sidebar_width = min(28, w // 4)
        main_width = w - sidebar_width - 1
        content_height = h - 4  # Header + status bar

        # Render notebooks sidebar
        self._render_notebooks_panel(
            x=1, y=2,
            width=sidebar_width,
            height=content_height,
            notebooks=notebooks,
            selected_idx=selected_notebook_idx,
            note_counts=note_counts,
            focused=(focus_panel == 'notebooks')
        )

        # Render notes panel
        self._render_notes_panel(
            x=sidebar_width + 1, y=2,
            width=main_width,
            height=content_height,
            notes=notes,
            selected_idx=selected_note_idx,
            focused=(focus_panel == 'notes')
        )

        # Status bar
        self._render_status_bar(w, h, status_message, len(notes))

        # End frame - single flush to terminal
        self.screen.end_frame()

    def _render_header(self, width: int) -> None:
        """Render the application header."""
        title = "NOTES TUI"
        shortcuts = "[?] Help  [q] Quit"

        header = self.screen.styled(
            self.screen.pad_right(f"  {title}", width - len(shortcuts) - 2) + shortcuts + "  ",
            self.screen.REVERSE
        )
        self.screen.write_at(1, 1, header)

    def _render_notebooks_panel(
        self,
        x: int, y: int,
        width: int, height: int,
        notebooks: List[Notebook],
        selected_idx: int,
        note_counts: dict,
        focused: bool
    ) -> None:
        """Render the notebooks sidebar."""
        # Panel title
        title_style = self.screen.BOLD if focused else ""
        title = self.screen.styled("NOTEBOOKS", title_style)
        self.screen.write_at(x, y, title)

        # Draw box
        box_y = y + 1
        box_height = min(len(notebooks) + 2, height - 3)
        self.screen.draw_box(x, box_y, width - 1, box_height)

        # Render notebook items
        for i, nb in enumerate(notebooks):
            if i >= box_height - 2:
                break

            count = note_counts.get(nb.id, 0)
            item_text = f" {nb.name} ({count})"
            item_text = self.screen.truncate(item_text, width - 5)

            if i == selected_idx:
                prefix = ">"
                if focused:
                    style = self.screen.REVERSE
                else:
                    style = self.screen.BOLD
            else:
                prefix = " "
                style = ""

            line = self.screen.styled(
                self.screen.pad_right(f"{prefix}{item_text}", width - 3),
                style
            )
            self.screen.write_at(x + 1, box_y + 1 + i, line)

        # Shortcut hint
        hint_y = box_y + box_height + 1
        if hint_y < y + height:
            self.screen.write_at(x, hint_y, self.screen.styled("[N] New Notebook", self.screen.DIM))

    def _render_notes_panel(
        self,
        x: int, y: int,
        width: int, height: int,
        notes: List[Note],
        selected_idx: int,
        focused: bool
    ) -> None:
        """Render the notes list panel."""
        # Panel title
        title_style = self.screen.BOLD if focused else ""
        title = self.screen.styled("NOTES", title_style)
        self.screen.write_at(x, y, title)

        # Draw box
        box_y = y + 1
        box_height = height - 4
        self.screen.draw_box(x, box_y, width - 1, box_height)

        if not notes:
            empty_msg = "No notes yet. Press 'n' to create one."
            self.screen.write_at(x + 2, box_y + 2, self.screen.styled(empty_msg, self.screen.DIM))
        else:
            # Render note items
            date_width = 12
            title_width = width - date_width - 8

            for i, note in enumerate(notes):
                if i >= box_height - 2:
                    break

                title_text = self.screen.truncate(note.title, title_width)
                date_text = note.updated_at.strftime("%Y-%m-%d")

                if i == selected_idx:
                    prefix = ">"
                    if focused:
                        style = self.screen.REVERSE
                    else:
                        style = self.screen.BOLD
                else:
                    prefix = " "
                    style = ""

                # Format: "> Title                    2026-01-14"
                line_content = f"{prefix} {title_text}"
                line_content = self.screen.pad_right(line_content, width - date_width - 5)
                line_content += date_text

                line = self.screen.styled(
                    self.screen.pad_right(line_content, width - 3),
                    style
                )
                self.screen.write_at(x + 1, box_y + 1 + i, line)

        # Shortcut hints
        hint_y = box_y + box_height + 1
        if hint_y < y + height:
            hints = "[n] New  [e] Edit  [d] Delete  [/] Search"
            self.screen.write_at(x, hint_y, self.screen.styled(hints, self.screen.DIM))

    def _render_status_bar(self, width: int, height: int, message: str, note_count: int) -> None:
        """Render the status bar at the bottom."""
        if message:
            status = f"  {message}"
        else:
            status = f"  {note_count} notes | Press ? for help"

        status_line = self.screen.styled(
            self.screen.pad_right(status, width),
            self.screen.REVERSE
        )
        self.screen.write_at(1, height, status_line)

    def render_editor(
        self,
        note: Note,
        cursor_line: int,
        cursor_col: int,
        scroll_offset: int,
        modified: bool
    ) -> None:
        """Render the note editor view."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Begin buffered frame (no flicker)
        self.screen.begin_frame()

        # Clear all lines
        for y in range(1, h + 1):
            self.screen.write_at(1, y, " " * w)

        # Header
        title_display = self.screen.truncate(f"EDITING: {note.title}", w - 30)
        shortcuts = "[Esc] Back  [^S] Save"
        header = self.screen.styled(
            self.screen.pad_right(f"  {title_display}", w - len(shortcuts) - 2) + shortcuts + "  ",
            self.screen.REVERSE
        )
        self.screen.write_at(1, 1, header)

        # Title field
        self.screen.write_at(3, 3, self.screen.pad_right(f"Title: {note.title}", w - 4))
        self.screen.write_at(3, 4, "─" * (w - 6))

        # Content area
        content_start_y = 6
        content_height = h - content_start_y - 2
        lines = note.content.split("\n")

        for i in range(content_height):
            line_idx = scroll_offset + i
            if line_idx < len(lines):
                line_text = self.screen.truncate(lines[line_idx], w - 6)
            else:
                line_text = ""
            self.screen.write_at(3, content_start_y + i, self.screen.pad_right(line_text, w - 6))

        # Status bar
        modified_text = "Modified" if modified else "Saved"
        nb_name = note.notebook_id
        status = f"  Line {cursor_line + 1}, Col {cursor_col + 1} | {modified_text} | Notebook: {nb_name}"
        status_line = self.screen.styled(
            self.screen.pad_right(status, w),
            self.screen.REVERSE
        )
        self.screen.write_at(1, h, status_line)

        # Show cursor position
        self.screen.show_cursor()
        display_line = cursor_line - scroll_offset
        if 0 <= display_line < content_height:
            self.screen.move_cursor(3 + cursor_col, content_start_y + display_line)

        # End frame - single flush to terminal
        self.screen.end_frame()

    def render_search(
        self,
        query: str,
        results: List[Note],
        selected_idx: int,
        notebook_names: dict
    ) -> None:
        """Render the search view."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Begin buffered frame (no flicker)
        self.screen.begin_frame()

        # Clear all lines
        for y in range(1, h + 1):
            self.screen.write_at(1, y, " " * w)

        # Header
        header = self.screen.styled(
            self.screen.pad_right("  SEARCH", w - 15) + "[Esc] Back  ",
            self.screen.REVERSE
        )
        self.screen.write_at(1, 1, header)

        # Search input
        self.screen.write_at(3, 3, self.screen.pad_right(f"Search: {query}_", w - 4))
        self.screen.write_at(3, 4, "─" * (w - 6))

        # Results
        if results:
            self.screen.write_at(3, 6, f"Results ({len(results)} matches):")

            box_y = 7
            box_height = min(len(results) * 3 + 2, h - box_y - 3)
            self.screen.draw_box(3, box_y, w - 6, box_height)

            result_y = box_y + 1
            for i, note in enumerate(results):
                if result_y >= box_y + box_height - 1:
                    break

                nb_name = notebook_names.get(note.notebook_id, note.notebook_id)

                if i == selected_idx:
                    prefix = ">"
                    style = self.screen.REVERSE
                else:
                    prefix = " "
                    style = ""

                # Title line
                title_line = f"{prefix} {note.title}"
                title_line = self.screen.truncate(title_line, w - 20)
                title_line = self.screen.pad_right(title_line, w - 20) + f"[{nb_name}]"
                self.screen.write_at(4, result_y, self.screen.styled(
                    self.screen.pad_right(title_line, w - 8),
                    style
                ))

                # Preview line
                preview = note.get_preview(w - 12)
                self.screen.write_at(6, result_y + 1, self.screen.styled(
                    self.screen.pad_right(f'"{preview}"', w - 10),
                    self.screen.DIM
                ))

                result_y += 3
        elif query:
            self.screen.write_at(3, 6, self.screen.styled("No results found.", self.screen.DIM))
        else:
            self.screen.write_at(3, 6, self.screen.styled("Type to search...", self.screen.DIM))

        # Hints
        hints = "[Enter] Open  [Tab] Next  [Esc] Cancel"
        self.screen.write_at(3, h - 1, self.screen.styled(hints, self.screen.DIM))

        # End frame - single flush to terminal
        self.screen.end_frame()

    def render_help(self) -> None:
        """Render the help dialog."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Dialog dimensions
        dialog_width = 50
        dialog_height = 26
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        # Draw dialog box
        self.screen.draw_box(x, y, dialog_width, dialog_height, "KEYBOARD SHORTCUTS", double=True)

        # Content
        lines = [
            "",
            "NAVIGATION",
            "───────────────────────────────────────────",
            "j / Down       Move down",
            "k / Up         Move up",
            "h / Left       Focus notebooks",
            "l / Right      Focus notes",
            "Enter          Select / Open",
            "Tab            Switch panels",
            "",
            "ACTIONS",
            "───────────────────────────────────────────",
            "n              New note",
            "N              New notebook",
            "e              Edit selected note",
            "d              Delete selected",
            "/              Search",
            "r              Rename notebook",
            "",
            "GENERAL",
            "───────────────────────────────────────────",
            "?              Show this help",
            "q              Quit application",
            "Esc            Cancel / Go back",
        ]

        for i, line in enumerate(lines):
            if i >= dialog_height - 3:
                break
            self.screen.write_at(x + 2, y + 1 + i, line[:dialog_width - 4])

        # Close hint
        close_hint = "[Press any key to close]"
        self.screen.write_at(x + (dialog_width - len(close_hint)) // 2, y + dialog_height - 2, close_hint)

    def render_confirm_dialog(self, message: str, options: str = "[y/n]") -> None:
        """Render a confirmation dialog."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        dialog_width = max(len(message) + 8, 40)
        dialog_height = 5
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        self.screen.draw_box(x, y, dialog_width, dialog_height, "CONFIRM")
        self.screen.write_at(x + 2, y + 2, message)
        self.screen.write_at(x + dialog_width - len(options) - 3, y + 2, options)

    def render_input_dialog(self, prompt: str, value: str) -> None:
        """Render an input dialog."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        dialog_width = max(len(prompt) + 20, 50)
        dialog_height = 5
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        self.screen.draw_box(x, y, dialog_width, dialog_height, "INPUT")
        self.screen.write_at(x + 2, y + 2, f"{prompt}: {value}_")

        self.screen.show_cursor()
        self.screen.move_cursor(x + len(prompt) + 4 + len(value), y + 2)
