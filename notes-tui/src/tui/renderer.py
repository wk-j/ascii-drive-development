"""
Renderer
========

Main rendering engine for the TUI application with Nerd Font icon support.

Layout (with icons):
+===========================================================================+
|  󰎚 NOTES TUI                                       󰋖 Help  󰗼 Quit       |
+===========================================================================+
|                          |                                                |
|   NOTEBOOKS             |  󰎞 NOTES                                        |
|  +-----------------+     |  +---------------------------------------------+
|  |  Default    (5)|     |  | 󰎞 My First Note              2026-01-14    |
|  |   Work       (3)|     |  | 󰎞 Shopping List              2026-01-13    |
|  |   Personal   (8)|     |  | 󰎞 Meeting Notes              2026-01-12    |
|  +-----------------+     |  +---------------------------------------------+
|                          |                                                |
+--------------------------+------------------------------------------------+
|  󰋚 Modified | 18 notes                                                    |
+===========================================================================+
"""

from typing import List, Optional, Callable
from datetime import datetime

from .screen import Screen
from .icons import icons
from ..models import Note, Notebook


class Renderer:
    """Renders the TUI interface with Nerd Font icons."""

    def __init__(self, screen: Screen):
        """Initialize renderer with a screen instance."""
        self.screen = screen
        self.icons = icons

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
        """Render the application header with icons."""
        title = f"{self.icons.app} NOTES TUI"
        shortcuts = f"{self.icons.help} Help  {self.icons.quit} Quit"

        # Account for icon width (icons are typically 1-2 chars wide visually)
        header_content = f"  {title}"
        shortcuts_section = f"{shortcuts}  "

        header = self.screen.styled(
            self.screen.pad_right(header_content, width - self.screen._visible_length(shortcuts_section)) + shortcuts_section,
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
        """Render the notebooks sidebar with icons."""
        # Panel title with icon
        title_style = self.screen.BOLD if focused else ""
        title = self.screen.styled(f"{self.icons.notebook} NOTEBOOKS", title_style)
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
            # Use folder icon for notebooks
            folder_icon = self.icons.folder_open if i == selected_idx else self.icons.folder
            item_text = f" {folder_icon} {nb.name} ({count})"
            item_text = self.screen.truncate(item_text, width - 4)

            if i == selected_idx:
                prefix = self.icons.chevron_right
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

        # Shortcut hint with icon
        hint_y = box_y + box_height + 1
        if hint_y < y + height:
            hint = f"{self.icons.add} [N] New Notebook"
            self.screen.write_at(x, hint_y, self.screen.styled(hint, self.screen.DIM))

    def _render_notes_panel(
        self,
        x: int, y: int,
        width: int, height: int,
        notes: List[Note],
        selected_idx: int,
        focused: bool
    ) -> None:
        """Render the notes list panel with icons."""
        # Panel title with icon
        title_style = self.screen.BOLD if focused else ""
        title = self.screen.styled(f"{self.icons.note} NOTES", title_style)
        self.screen.write_at(x, y, title)

        # Draw box
        box_y = y + 1
        box_height = height - 4
        self.screen.draw_box(x, box_y, width - 1, box_height)

        if not notes:
            empty_msg = f"No notes yet. Press 'n' to create one."
            self.screen.write_at(x + 2, box_y + 2, self.screen.styled(empty_msg, self.screen.DIM))
        else:
            # Render note items
            date_width = 12
            title_width = width - date_width - 10  # Extra space for icons

            for i, note in enumerate(notes):
                if i >= box_height - 2:
                    break

                title_text = self.screen.truncate(note.title, title_width)
                date_text = f"{self.icons.calendar} {note.updated_at.strftime('%Y-%m-%d')}"

                if i == selected_idx:
                    prefix = self.icons.chevron_right
                    note_icon = self.icons.note
                    if focused:
                        style = self.screen.REVERSE
                    else:
                        style = self.screen.BOLD
                else:
                    prefix = " "
                    note_icon = self.icons.note
                    style = ""

                # Format: "> 󰎞 Title                    📅 2026-01-14"
                line_content = f"{prefix} {note_icon} {title_text}"
                line_content = self.screen.pad_right(line_content, width - date_width - 7)
                line_content += date_text

                line = self.screen.styled(
                    self.screen.pad_right(line_content, width - 3),
                    style
                )
                self.screen.write_at(x + 1, box_y + 1 + i, line)

        # Shortcut hints with icons
        hint_y = box_y + box_height + 1
        if hint_y < y + height:
            hints = f"{self.icons.add}[n] New  {self.icons.edit}[e] Edit  {self.icons.delete}[d] Del  {self.icons.search}[/] Search"
            self.screen.write_at(x, hint_y, self.screen.styled(hints, self.screen.DIM))

    def _render_status_bar(self, width: int, height: int, message: str, note_count: int) -> None:
        """Render the status bar at the bottom with icons."""
        if message:
            # Determine icon based on message content
            if "deleted" in message.lower():
                icon = self.icons.delete
            elif "saved" in message.lower():
                icon = self.icons.saved
            elif "created" in message.lower():
                icon = self.icons.add
            else:
                icon = self.icons.info
            status = f"  {icon} {message}"
        else:
            status = f"  {self.icons.note} {note_count} notes │ {self.icons.help} Press ? for help"

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
        """Render the note editor view with icons."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Begin buffered frame (no flicker)
        self.screen.begin_frame()

        # Clear all lines
        for y in range(1, h + 1):
            self.screen.write_at(1, y, " " * w)

        # Header with icons
        title_display = self.screen.truncate(f"{self.icons.edit} EDITING: {note.title}", w - 35)
        shortcuts = f"{self.icons.back} [Esc] Back  {self.icons.save} [^S] Save"
        header = self.screen.styled(
            self.screen.pad_right(f"  {title_display}", w - self.screen._visible_length(shortcuts) - 2) + shortcuts + "  ",
            self.screen.REVERSE
        )
        self.screen.write_at(1, 1, header)

        # Title field with icon
        self.screen.write_at(3, 3, self.screen.pad_right(f"{self.icons.tag} Title: {note.title}", w - 4))
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

        # Status bar with icons
        status_icon = self.icons.modified if modified else self.icons.saved
        modified_text = "Modified" if modified else "Saved"
        nb_name = note.notebook_id
        status = f"  Line {cursor_line + 1}, Col {cursor_col + 1} │ {status_icon} {modified_text} │ {self.icons.folder} {nb_name}"
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
        """Render the search view with icons."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Begin buffered frame (no flicker)
        self.screen.begin_frame()

        # Clear all lines
        for y in range(1, h + 1):
            self.screen.write_at(1, y, " " * w)

        # Header with icon
        shortcuts = f"{self.icons.back} [Esc] Back"
        header = self.screen.styled(
            self.screen.pad_right(f"  {self.icons.search} SEARCH", w - self.screen._visible_length(shortcuts) - 2) + shortcuts + "  ",
            self.screen.REVERSE
        )
        self.screen.write_at(1, 1, header)

        # Search input with icon
        self.screen.write_at(3, 3, self.screen.pad_right(f"{self.icons.search} Search: {query}_", w - 4))
        self.screen.write_at(3, 4, "─" * (w - 6))

        # Results
        if results:
            self.screen.write_at(3, 6, f"{self.icons.success} Results ({len(results)} matches):")

            box_y = 7
            box_height = min(len(results) * 3 + 2, h - box_y - 3)
            self.screen.draw_box(3, box_y, w - 6, box_height)

            result_y = box_y + 1
            for i, note in enumerate(results):
                if result_y >= box_y + box_height - 1:
                    break

                nb_name = notebook_names.get(note.notebook_id, note.notebook_id)

                if i == selected_idx:
                    prefix = self.icons.chevron_right
                    style = self.screen.REVERSE
                else:
                    prefix = " "
                    style = ""

                # Title line with icon
                title_line = f"{prefix} {self.icons.note} {note.title}"
                title_line = self.screen.truncate(title_line, w - 22)
                title_line = self.screen.pad_right(title_line, w - 22) + f"[{self.icons.folder} {nb_name}]"
                self.screen.write_at(4, result_y, self.screen.styled(
                    self.screen.pad_right(title_line, w - 8),
                    style
                ))

                # Preview line
                preview = note.get_preview(w - 14)
                self.screen.write_at(6, result_y + 1, self.screen.styled(
                    self.screen.pad_right(f'"{preview}"', w - 10),
                    self.screen.DIM
                ))

                result_y += 3
        elif query:
            self.screen.write_at(3, 6, self.screen.styled(f"{self.icons.warning} No results found.", self.screen.DIM))
        else:
            self.screen.write_at(3, 6, self.screen.styled(f"{self.icons.info} Type to search...", self.screen.DIM))

        # Hints with icons
        hints = f"[Enter] Open  [Tab] Next  {self.icons.back} [Esc] Cancel"
        self.screen.write_at(3, h - 1, self.screen.styled(hints, self.screen.DIM))

        # End frame - single flush to terminal
        self.screen.end_frame()

    def render_help(self) -> None:
        """Render the help dialog with icons."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        # Dialog dimensions
        dialog_width = 52
        dialog_height = 26
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        # Draw dialog box
        self.screen.draw_box(x, y, dialog_width, dialog_height, f"{self.icons.help} KEYBOARD SHORTCUTS", double=True)

        # Content with icons
        lines = [
            "",
            f"{self.icons.arrow_down} NAVIGATION",
            "───────────────────────────────────────────────",
            f"  {self.icons.arrow_down} j / Down       Move down",
            f"  {self.icons.arrow_up} k / Up         Move up",
            f"  {self.icons.arrow_left} h / Left       Focus notebooks",
            f"  {self.icons.arrow_right} l / Right      Focus notes",
            f"  {self.icons.chevron_right} Enter          Select / Open",
            "    Tab            Switch panels",
            "",
            f"{self.icons.edit} ACTIONS",
            "───────────────────────────────────────────────",
            f"  {self.icons.add} n              New note",
            f"  {self.icons.notebook} N              New notebook",
            f"  {self.icons.edit} e              Edit selected note",
            f"  {self.icons.delete} d              Delete selected",
            f"  {self.icons.search} /              Search",
            f"  {self.icons.tag} r              Rename notebook",
            "",
            f"{self.icons.info} GENERAL",
            "───────────────────────────────────────────────",
            f"  {self.icons.help} ?              Show this help",
            f"  {self.icons.quit} q              Quit application",
            f"  {self.icons.back} Esc            Cancel / Go back",
        ]

        for i, line in enumerate(lines):
            if i >= dialog_height - 3:
                break
            self.screen.write_at(x + 2, y + 1 + i, line[:dialog_width - 4])

        # Close hint
        close_hint = "[Press any key to close]"
        self.screen.write_at(x + (dialog_width - len(close_hint)) // 2, y + dialog_height - 2, close_hint)

    def render_confirm_dialog(self, message: str, options: str = "[y/n]") -> None:
        """Render a confirmation dialog with icon."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        dialog_width = max(len(message) + 12, 44)
        dialog_height = 5
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        self.screen.draw_box(x, y, dialog_width, dialog_height, f"{self.icons.warning} CONFIRM")
        self.screen.write_at(x + 2, y + 2, f"{self.icons.warning} {message}")
        self.screen.write_at(x + dialog_width - len(options) - 3, y + 2, options)

    def render_input_dialog(self, prompt: str, value: str) -> None:
        """Render an input dialog with icon."""
        self.screen.update_size()
        w, h = self.screen.width, self.screen.height

        dialog_width = max(len(prompt) + 24, 54)
        dialog_height = 5
        x = (w - dialog_width) // 2
        y = (h - dialog_height) // 2

        self.screen.draw_box(x, y, dialog_width, dialog_height, f"{self.icons.edit} INPUT")
        self.screen.write_at(x + 2, y + 2, f"{self.icons.edit} {prompt}: {value}_")

        self.screen.show_cursor()
        self.screen.move_cursor(x + len(prompt) + 7 + len(value), y + 2)
