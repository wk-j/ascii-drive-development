# Notes TUI

A terminal-based note taking application built with **ASCII Driven Development** methodology.

```
+===========================================================================+
|  󰎚 NOTES TUI                                       󰋖 Help  󰗼 Quit       |
+===========================================================================+
|                          |                                                |
|   NOTEBOOKS             |  󰎞 NOTES                                        |
|  +-----------------+     |  +---------------------------------------------+
|  |  Default    (5)|     |  | 󰎞 My First Note               2026-01-14  |
|  |   Work       (3)|     |  | 󰎞 Shopping List               2026-01-13  |
|  +-----------------+     |  +---------------------------------------------+
|                          |                                                |
+===========================================================================+
```

## Features

- Create, edit, and delete notes
- Organize notes in notebooks
- Search notes by title and content
- Full keyboard navigation (vim-style)
- Persistent JSON storage
- **Nerd Font icons** with Unicode/ASCII fallback
- Double-buffered rendering (no flicker)
- Clean, modern TUI interface

## Requirements

- Python 3.8+
- Unix-like terminal (macOS, Linux)
- **Recommended:** Terminal with [Nerd Font](https://www.nerdfonts.com/) for best icon display

## Installation

```bash
cd notes-tui
```

No additional dependencies required - uses only Python standard library.

## Usage

```bash
# Run from the notes-tui directory
python -m src.main

# Or specify a custom data path
python -m src.main --data-path /path/to/notes.json

# Force specific icon mode
NOTES_TUI_ICONS=ascii python -m src.main   # ASCII fallback
NOTES_TUI_ICONS=unicode python -m src.main  # Unicode icons
NOTES_TUI_ICONS=nerd python -m src.main     # Nerd Font icons (default)
```

## Icon Support

Notes TUI supports three icon modes:

| Mode | Description | Example |
|------|-------------|---------|
| `nerd` | Nerd Font icons (default) | 󰎚 󰎞  󰍉 |
| `unicode` | Standard Unicode symbols | 📓 📝 📁 🔍 |
| `ascii` | Plain ASCII fallback | [N] * [D] / |

Set the `NOTES_TUI_ICONS` environment variable to change modes:
```bash
export NOTES_TUI_ICONS=nerd    # Best visuals (requires Nerd Font)
export NOTES_TUI_ICONS=unicode # Good fallback for most terminals
export NOTES_TUI_ICONS=ascii   # Works everywhere
```

## Keyboard Shortcuts

```
+-----------------------------------------------+
|                KEYBOARD SHORTCUTS             |
+-----------------------------------------------+
|                                               |
|  NAVIGATION                                   |
|  ------------------------------------------- |
|  j / Down      Move down                      |
|  k / Up        Move up                        |
|  h / Left      Focus notebooks                |
|  l / Right     Focus notes                    |
|  Enter         Select / Open                  |
|  Tab           Switch panels                  |
|                                               |
|  ACTIONS                                      |
|  ------------------------------------------- |
|  n             New note                       |
|  N             New notebook                   |
|  e             Edit selected note             |
|  d             Delete selected                |
|  /             Search                         |
|                                               |
|  EDITOR                                       |
|  ------------------------------------------- |
|  Ctrl+S        Save note                      |
|  Esc           Exit editor (auto-saves)       |
|  Arrow keys    Navigate                       |
|                                               |
|  GENERAL                                      |
|  ------------------------------------------- |
|  ?             Show help                      |
|  q             Quit application               |
|  Esc           Cancel / Go back               |
+-----------------------------------------------+
```

## Screen Layout

### Main View

```
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
|  Status: 18 notes | Press ? for help                                     |
+===========================================================================+
```

### Editor View

```
+===========================================================================+
|  EDITING: My First Note                            [Esc] Back  [^S] Save |
+===========================================================================+
|                                                                           |
|  Title: My First Note                                                     |
|  -----------------------------------------------------------------------  |
|                                                                           |
|  This is my first note in the Notes TUI application.                     |
|                                                                           |
|  _                                                                        |
|                                                                           |
+===========================================================================+
|  Line 1, Col 1 | Saved | Notebook: Default                               |
+===========================================================================+
```

## Data Storage

Notes are stored in JSON format at `data/notes.json`:

```json
{
  "notebooks": [
    {
      "id": "default",
      "name": "Default",
      "created_at": "2026-01-14T10:00:00",
      "updated_at": "2026-01-14T10:00:00"
    }
  ],
  "notes": [
    {
      "id": "note_abc123",
      "notebook_id": "default",
      "title": "My Note",
      "content": "Note content here...",
      "created_at": "2026-01-14T10:00:00",
      "updated_at": "2026-01-14T10:00:00"
    }
  ]
}
```

## Project Structure

```
notes-tui/
|
+-- src/
|   +-- main.py              # Application entry point
|   +-- app.py               # Main application class
|   |
|   +-- models/
|   |   +-- note.py          # Note data model
|   |   +-- notebook.py      # Notebook data model
|   |
|   +-- storage/
|   |   +-- repository.py    # Data persistence
|   |
|   +-- tui/
|       +-- screen.py        # Terminal screen (double-buffered)
|       +-- renderer.py      # UI rendering with icons
|       +-- input_handler.py # Keyboard input
|       +-- icons.py         # Nerd Font/Unicode/ASCII icons
|
+-- data/
|   +-- notes.json           # Persistent storage
|
+-- DESIGN.md                # ASCII Driven Development design doc
+-- README.md                # This file
```

## Development

This project was built following the **ASCII Driven Development** methodology:

1. All designs created using ASCII diagrams
2. Documentation lives alongside code
3. Version control friendly (no binary formats)
4. Universal readability

See `DESIGN.md` for the complete design documentation.

## License

MIT License
