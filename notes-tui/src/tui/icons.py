"""
Icons Module
============

Nerd Font icons with ASCII fallbacks for terminals without Nerd Font support.

Nerd Font Reference: https://www.nerdfonts.com/cheat-sheet

Icon Categories:
+------------------+------------------+------------------+
|   App Icons      |   Action Icons   |   Status Icons   |
+------------------+------------------+------------------+
|  󰎚 Note          |  󰐕 Add           |   Success       |
|   Notebook      |   Edit          |   Warning       |
|  󰍉 Search        |  󰆴 Delete        |   Error         |
|   Folder        |   Save          |  󰋚 Modified      |
+------------------+------------------+------------------+
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class IconSet:
    """A set of icons with Nerd Font and ASCII versions."""

    # Application
    app: str
    note: str
    notebook: str
    folder: str
    folder_open: str

    # Actions
    add: str
    edit: str
    delete: str
    save: str
    search: str
    help: str
    quit: str
    back: str

    # Navigation
    arrow_right: str
    arrow_left: str
    arrow_up: str
    arrow_down: str
    chevron_right: str
    chevron_down: str

    # Status
    success: str
    warning: str
    error: str
    info: str
    modified: str
    saved: str

    # UI Elements
    bullet: str
    checkbox_empty: str
    checkbox_checked: str
    star: str
    pin: str
    calendar: str
    clock: str
    tag: str


# Nerd Font icons (requires Nerd Font installed)
NERD_FONT_ICONS = IconSet(
    # Application
    app="󰎚",           # nf-md-notebook
    note="󰎞",          # nf-md-note_text
    notebook="",       # nf-oct-book
    folder="",         # nf-fa-folder
    folder_open="",   # nf-fa-folder_open

    # Actions
    add="󰐕",           # nf-md-plus_circle
    edit="",          # nf-fa-pencil
    delete="󰆴",        # nf-md-delete
    save="󰆓",          # nf-md-content_save
    search="󰍉",        # nf-md-magnify
    help="󰋖",          # nf-md-help_circle
    quit="󰗼",          # nf-md-exit_to_app
    back="󰁍",          # nf-md-arrow_left

    # Navigation
    arrow_right="",   # nf-fa-arrow_right
    arrow_left="",    # nf-fa-arrow_left
    arrow_up="",      # nf-fa-arrow_up
    arrow_down="",    # nf-fa-arrow_down
    chevron_right="", # nf-oct-chevron_right
    chevron_down="",  # nf-oct-chevron_down

    # Status
    success="",       # nf-fa-check
    warning="",       # nf-fa-exclamation_triangle
    error="",         # nf-fa-times_circle
    info="",          # nf-fa-info_circle
    modified="󰋚",      # nf-md-circle_edit_outline
    saved="󰄬",         # nf-md-check_circle

    # UI Elements
    bullet="",        # nf-oct-dot_fill
    checkbox_empty="󰄱", # nf-md-checkbox_blank_outline
    checkbox_checked="󰄵", # nf-md-checkbox_marked
    star="",          # nf-fa-star
    pin="󰐃",           # nf-md-pin
    calendar="",      # nf-fa-calendar
    clock="",         # nf-fa-clock_o
    tag="󰓹",           # nf-md-tag
)

# ASCII fallback icons (works in any terminal)
ASCII_ICONS = IconSet(
    # Application
    app="[N]",
    note="*",
    notebook="#",
    folder="[D]",
    folder_open="[D]",

    # Actions
    add="+",
    edit="~",
    delete="x",
    save="S",
    search="/",
    help="?",
    quit="Q",
    back="<",

    # Navigation
    arrow_right="->",
    arrow_left="<-",
    arrow_up="^",
    arrow_down="v",
    chevron_right=">",
    chevron_down="v",

    # Status
    success="[OK]",
    warning="[!]",
    error="[X]",
    info="[i]",
    modified="[*]",
    saved="[S]",

    # UI Elements
    bullet="*",
    checkbox_empty="[ ]",
    checkbox_checked="[x]",
    star="*",
    pin="^",
    calendar="[C]",
    clock="@",
    tag="#",
)

# Unicode fallback (works in most modern terminals)
UNICODE_ICONS = IconSet(
    # Application
    app="📓",
    note="📝",
    notebook="📖",
    folder="📁",
    folder_open="📂",

    # Actions
    add="➕",
    edit="✏️",
    delete="🗑️",
    save="💾",
    search="🔍",
    help="❓",
    quit="🚪",
    back="◀",

    # Navigation
    arrow_right="→",
    arrow_left="←",
    arrow_up="↑",
    arrow_down="↓",
    chevron_right="›",
    chevron_down="˅",

    # Status
    success="✓",
    warning="⚠",
    error="✗",
    info="ℹ",
    modified="●",
    saved="✓",

    # UI Elements
    bullet="•",
    checkbox_empty="☐",
    checkbox_checked="☑",
    star="★",
    pin="📌",
    calendar="📅",
    clock="⏰",
    tag="🏷",
)


class Icons:
    """Icon provider with automatic fallback detection."""

    def __init__(self, mode: Optional[str] = None):
        """
        Initialize icons with specified or auto-detected mode.

        Args:
            mode: 'nerd', 'unicode', 'ascii', or None for auto-detect
        """
        if mode is None:
            mode = self._detect_mode()

        self._mode = mode
        self._icons = self._get_icon_set(mode)

    def _detect_mode(self) -> str:
        """Auto-detect the best icon mode based on environment."""
        # Check environment variable
        icon_mode = os.environ.get('NOTES_TUI_ICONS', '').lower()
        if icon_mode in ('nerd', 'unicode', 'ascii'):
            return icon_mode

        # Check for Nerd Font hint
        if os.environ.get('NERD_FONTS'):
            return 'nerd'

        # Check terminal type
        term = os.environ.get('TERM', '')
        term_program = os.environ.get('TERM_PROGRAM', '')

        # Known terminals with good Unicode/Nerd Font support
        nerd_friendly = ['kitty', 'alacritty', 'wezterm', 'iterm', 'iterm2']
        if any(t in term_program.lower() for t in nerd_friendly):
            return 'nerd'

        # Default to nerd fonts (most modern terminals support them)
        # Users can set NOTES_TUI_ICONS=ascii if needed
        return 'nerd'

    def _get_icon_set(self, mode: str) -> IconSet:
        """Get the icon set for the specified mode."""
        if mode == 'nerd':
            return NERD_FONT_ICONS
        elif mode == 'unicode':
            return UNICODE_ICONS
        else:
            return ASCII_ICONS

    @property
    def mode(self) -> str:
        """Get current icon mode."""
        return self._mode

    def set_mode(self, mode: str) -> None:
        """Change icon mode."""
        self._mode = mode
        self._icons = self._get_icon_set(mode)

    # Convenience accessors
    @property
    def app(self) -> str: return self._icons.app
    @property
    def note(self) -> str: return self._icons.note
    @property
    def notebook(self) -> str: return self._icons.notebook
    @property
    def folder(self) -> str: return self._icons.folder
    @property
    def folder_open(self) -> str: return self._icons.folder_open
    @property
    def add(self) -> str: return self._icons.add
    @property
    def edit(self) -> str: return self._icons.edit
    @property
    def delete(self) -> str: return self._icons.delete
    @property
    def save(self) -> str: return self._icons.save
    @property
    def search(self) -> str: return self._icons.search
    @property
    def help(self) -> str: return self._icons.help
    @property
    def quit(self) -> str: return self._icons.quit
    @property
    def back(self) -> str: return self._icons.back
    @property
    def arrow_right(self) -> str: return self._icons.arrow_right
    @property
    def arrow_left(self) -> str: return self._icons.arrow_left
    @property
    def arrow_up(self) -> str: return self._icons.arrow_up
    @property
    def arrow_down(self) -> str: return self._icons.arrow_down
    @property
    def chevron_right(self) -> str: return self._icons.chevron_right
    @property
    def chevron_down(self) -> str: return self._icons.chevron_down
    @property
    def success(self) -> str: return self._icons.success
    @property
    def warning(self) -> str: return self._icons.warning
    @property
    def error(self) -> str: return self._icons.error
    @property
    def info(self) -> str: return self._icons.info
    @property
    def modified(self) -> str: return self._icons.modified
    @property
    def saved(self) -> str: return self._icons.saved
    @property
    def bullet(self) -> str: return self._icons.bullet
    @property
    def checkbox_empty(self) -> str: return self._icons.checkbox_empty
    @property
    def checkbox_checked(self) -> str: return self._icons.checkbox_checked
    @property
    def star(self) -> str: return self._icons.star
    @property
    def pin(self) -> str: return self._icons.pin
    @property
    def calendar(self) -> str: return self._icons.calendar
    @property
    def clock(self) -> str: return self._icons.clock
    @property
    def tag(self) -> str: return self._icons.tag


# Global icons instance
icons = Icons()
