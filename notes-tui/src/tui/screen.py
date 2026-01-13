"""
Screen Management
=================

Handles terminal screen operations with double buffering to prevent flicker.

Double Buffering Strategy:
+------------------+     +------------------+     +------------------+
|   Application    | --> |   Back Buffer    | --> |   Terminal       |
|   (draw calls)   |     |   (in memory)    |     |   (single flush) |
+------------------+     +------------------+     +------------------+

Instead of:  clear screen → draw (causes flicker)
We do:       move home → overwrite → single flush (no flicker)
"""

import os
import sys
import termios
import tty
from typing import Tuple, Optional, List


class Screen:
    """Manages terminal screen operations with double buffering."""

    # ANSI escape codes
    ESC = "\033"
    CSI = f"{ESC}["

    # Cursor control
    CURSOR_HOME = f"{CSI}H"
    CURSOR_HIDE = f"{CSI}?25l"
    CURSOR_SHOW = f"{CSI}?25h"

    # Screen control
    CLEAR_SCREEN = f"{CSI}2J"
    CLEAR_LINE = f"{CSI}2K"

    # Colors
    RESET = f"{CSI}0m"
    BOLD = f"{CSI}1m"
    DIM = f"{CSI}2m"
    ITALIC = f"{CSI}3m"
    UNDERLINE = f"{CSI}4m"
    REVERSE = f"{CSI}7m"

    # Foreground colors
    FG_BLACK = f"{CSI}30m"
    FG_RED = f"{CSI}31m"
    FG_GREEN = f"{CSI}32m"
    FG_YELLOW = f"{CSI}33m"
    FG_BLUE = f"{CSI}34m"
    FG_MAGENTA = f"{CSI}35m"
    FG_CYAN = f"{CSI}36m"
    FG_WHITE = f"{CSI}37m"

    # Background colors
    BG_BLACK = f"{CSI}40m"
    BG_RED = f"{CSI}41m"
    BG_GREEN = f"{CSI}42m"
    BG_YELLOW = f"{CSI}43m"
    BG_BLUE = f"{CSI}44m"
    BG_MAGENTA = f"{CSI}45m"
    BG_CYAN = f"{CSI}46m"
    BG_WHITE = f"{CSI}47m"

    def __init__(self):
        """Initialize screen with double buffering."""
        self._old_settings: Optional[list] = None
        self.width, self.height = self.get_size()

        # Double buffering
        self._buffer: List[str] = []
        self._buffering = False

    def get_size(self) -> Tuple[int, int]:
        """Get terminal size (width, height)."""
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return 80, 24  # Default fallback

    def update_size(self) -> None:
        """Update stored terminal size."""
        self.width, self.height = self.get_size()

    def enter_raw_mode(self) -> None:
        """Enter raw terminal mode for direct key input."""
        if sys.stdin.isatty():
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())

    def exit_raw_mode(self) -> None:
        """Exit raw terminal mode."""
        if self._old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
            self._old_settings = None

    def enter_alternate_screen(self) -> None:
        """Enter alternate screen buffer."""
        sys.stdout.write(f"{self.CSI}?1049h")
        sys.stdout.flush()

    def exit_alternate_screen(self) -> None:
        """Exit alternate screen buffer."""
        sys.stdout.write(f"{self.CSI}?1049l")
        sys.stdout.flush()

    # ==================== Double Buffering ====================

    def begin_frame(self) -> None:
        """Begin a new frame - start buffering output."""
        self._buffer = []
        self._buffering = True
        # Move cursor home instead of clearing (prevents flicker)
        self._buffer.append(self.CURSOR_HOME)

    def end_frame(self) -> None:
        """End frame - flush all buffered output at once."""
        if self._buffering:
            # Clear any remaining content on screen by filling with spaces
            # This is handled by pad_right in rendering
            output = "".join(self._buffer)
            sys.stdout.write(output)
            sys.stdout.flush()
            self._buffer = []
            self._buffering = False

    def _write_to_buffer(self, text: str) -> None:
        """Write to buffer or directly to stdout."""
        if self._buffering:
            self._buffer.append(text)
        else:
            sys.stdout.write(text)
            sys.stdout.flush()

    # ==================== Screen Operations ====================

    def clear(self) -> None:
        """Clear the screen (only use for initial setup, not per-frame)."""
        if self._buffering:
            self._buffer.append(self.CLEAR_SCREEN + self.CURSOR_HOME)
        else:
            sys.stdout.write(self.CLEAR_SCREEN + self.CURSOR_HOME)
            sys.stdout.flush()

    def hide_cursor(self) -> None:
        """Hide the cursor."""
        self._write_to_buffer(self.CURSOR_HIDE)

    def show_cursor(self) -> None:
        """Show the cursor."""
        self._write_to_buffer(self.CURSOR_SHOW)

    def move_cursor(self, x: int, y: int) -> None:
        """Move cursor to position (1-indexed)."""
        self._write_to_buffer(f"{self.CSI}{y};{x}H")

    def write(self, text: str) -> None:
        """Write text to the terminal."""
        self._write_to_buffer(text)

    def write_at(self, x: int, y: int, text: str) -> None:
        """Write text at a specific position."""
        self._write_to_buffer(f"{self.CSI}{y};{x}H{text}")

    def write_line(self, y: int, text: str) -> None:
        """Write a full line, padding to screen width to overwrite old content."""
        padded = self.pad_right(text, self.width)
        self.write_at(1, y, padded)

    def draw_box(self, x: int, y: int, width: int, height: int,
                 title: str = "", double: bool = False) -> None:
        """Draw a box at the specified position."""
        if double:
            tl, tr, bl, br = "╔", "╗", "╚", "╝"
            h, v = "═", "║"
        else:
            tl, tr, bl, br = "┌", "┐", "└", "┘"
            h, v = "─", "│"

        # Top border
        if title:
            title_text = f" {title} "
            padding = width - 2 - len(title_text)
            if padding < 0:
                padding = 0
                title_text = title_text[:width-2]
            top = tl + title_text + h * padding + tr
        else:
            top = tl + h * (width - 2) + tr

        self.write_at(x, y, top)

        # Side borders with content clearing
        for i in range(1, height - 1):
            self.write_at(x, y + i, v + " " * (width - 2) + v)

        # Bottom border
        bottom = bl + h * (width - 2) + br
        self.write_at(x, y + height - 1, bottom)

    def fill_rect(self, x: int, y: int, width: int, height: int, char: str = " ") -> None:
        """Fill a rectangular area with a character."""
        line = char * width
        for i in range(height):
            self.write_at(x, y + i, line)

    def clear_line(self, y: int) -> None:
        """Clear a specific line."""
        self.write_at(1, y, " " * self.width)

    # ==================== Text Utilities ====================

    def styled(self, text: str, *styles: str) -> str:
        """Return text with ANSI styles applied."""
        if not styles:
            return text
        return "".join(styles) + text + self.RESET

    def truncate(self, text: str, max_width: int, suffix: str = "...") -> str:
        """Truncate text to fit within max_width."""
        if len(text) <= max_width:
            return text
        if max_width <= len(suffix):
            return text[:max_width]
        return text[:max_width - len(suffix)] + suffix

    def pad_right(self, text: str, width: int) -> str:
        """Pad text with spaces on the right to fill width."""
        # Calculate visible length (excluding ANSI codes)
        visible_len = self._visible_length(text)
        if visible_len >= width:
            return text
        return text + " " * (width - visible_len)

    def _visible_length(self, text: str) -> int:
        """Calculate visible length of text, excluding ANSI escape codes."""
        import re
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        clean_text = ansi_escape.sub('', text)
        return len(clean_text)

    def center(self, text: str, width: int) -> str:
        """Center text within the given width."""
        visible_len = self._visible_length(text)
        if visible_len >= width:
            return text
        padding = (width - visible_len) // 2
        return " " * padding + text + " " * (width - visible_len - padding)
