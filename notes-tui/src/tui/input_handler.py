"""
Input Handler
=============

Handles keyboard input in raw terminal mode.

Key Mapping:
+-----------------------------------------------+
|                KEYBOARD SHORTCUTS             |
+-----------------------------------------------+
|  j / Down      Move down                      |
|  k / Up        Move up                        |
|  h / Left      Focus notebooks                |
|  l / Right     Focus notes                    |
|  Enter         Select / Open                  |
|  Tab           Switch panels                  |
|  n             New note                       |
|  N             New notebook                   |
|  e             Edit selected note             |
|  d             Delete selected                |
|  /             Search                         |
|  ?             Show help                      |
|  q / Q         Quit application               |
|  Esc           Cancel / Go back               |
+-----------------------------------------------+
"""

import sys
import select
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Key(Enum):
    """Enumeration of recognized key types."""
    # Navigation
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    HOME = auto()
    END = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()

    # Actions
    ENTER = auto()
    TAB = auto()
    ESCAPE = auto()
    BACKSPACE = auto()
    DELETE = auto()

    # Control keys
    CTRL_C = auto()
    CTRL_D = auto()
    CTRL_S = auto()
    CTRL_Q = auto()
    CTRL_N = auto()

    # Character input
    CHAR = auto()

    # Unknown
    UNKNOWN = auto()


@dataclass
class KeyEvent:
    """Represents a keyboard event."""
    key: Key
    char: str = ""

    @property
    def is_printable(self) -> bool:
        """Check if the key is a printable character."""
        return self.key == Key.CHAR and len(self.char) == 1 and self.char.isprintable()


class InputHandler:
    """Handles keyboard input from the terminal."""

    # Escape sequences for special keys
    ESCAPE_SEQUENCES = {
        "[A": Key.UP,
        "[B": Key.DOWN,
        "[C": Key.RIGHT,
        "[D": Key.LEFT,
        "[H": Key.HOME,
        "[F": Key.END,
        "[5~": Key.PAGE_UP,
        "[6~": Key.PAGE_DOWN,
        "[3~": Key.DELETE,
        "OP": Key.UNKNOWN,  # F1
        "OQ": Key.UNKNOWN,  # F2
        "OR": Key.UNKNOWN,  # F3
        "OS": Key.UNKNOWN,  # F4
    }

    def __init__(self):
        """Initialize input handler."""
        pass

    def read_key(self, timeout: float = 0.1) -> Optional[KeyEvent]:
        """Read a single key press with optional timeout."""
        # Check if input is available
        if not self._has_input(timeout):
            return None

        # Read first character
        ch = self._read_char()
        if ch is None:
            return None

        # Handle escape sequences
        if ch == "\x1b":  # ESC
            return self._handle_escape_sequence()

        # Handle control characters
        if ord(ch) < 32:
            return self._handle_control_char(ch)

        # Handle backspace (some terminals send 127)
        if ord(ch) == 127:
            return KeyEvent(Key.BACKSPACE)

        # Regular character
        return KeyEvent(Key.CHAR, ch)

    def _has_input(self, timeout: float) -> bool:
        """Check if input is available within timeout."""
        readable, _, _ = select.select([sys.stdin], [], [], timeout)
        return bool(readable)

    def _read_char(self) -> Optional[str]:
        """Read a single character from stdin."""
        try:
            return sys.stdin.read(1)
        except (IOError, OSError):
            return None

    def _handle_escape_sequence(self) -> KeyEvent:
        """Handle escape sequences (arrow keys, function keys, etc.)."""
        # Check for additional characters with very short timeout
        if not self._has_input(0.05):
            return KeyEvent(Key.ESCAPE)

        seq = ""
        while self._has_input(0.01):
            ch = self._read_char()
            if ch is None:
                break
            seq += ch
            # Check if we have a complete sequence
            if seq in self.ESCAPE_SEQUENCES:
                return KeyEvent(self.ESCAPE_SEQUENCES[seq])
            # Limit sequence length
            if len(seq) > 6:
                break

        # Check for known sequence
        if seq in self.ESCAPE_SEQUENCES:
            return KeyEvent(self.ESCAPE_SEQUENCES[seq])

        return KeyEvent(Key.ESCAPE)

    def _handle_control_char(self, ch: str) -> KeyEvent:
        """Handle control characters."""
        code = ord(ch)

        if code == 3:  # Ctrl+C
            return KeyEvent(Key.CTRL_C)
        elif code == 4:  # Ctrl+D
            return KeyEvent(Key.CTRL_D)
        elif code == 9:  # Tab
            return KeyEvent(Key.TAB)
        elif code == 10 or code == 13:  # Enter (LF or CR)
            return KeyEvent(Key.ENTER)
        elif code == 14:  # Ctrl+N
            return KeyEvent(Key.CTRL_N)
        elif code == 17:  # Ctrl+Q
            return KeyEvent(Key.CTRL_Q)
        elif code == 19:  # Ctrl+S
            return KeyEvent(Key.CTRL_S)
        elif code == 127 or code == 8:  # Backspace
            return KeyEvent(Key.BACKSPACE)

        return KeyEvent(Key.UNKNOWN)

    def wait_for_key(self) -> KeyEvent:
        """Wait indefinitely for a key press."""
        while True:
            event = self.read_key(timeout=1.0)
            if event is not None:
                return event
