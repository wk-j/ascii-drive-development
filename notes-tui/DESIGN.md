# Notes TUI - ASCII Driven Development Design Document

```
+==========================================================================+
|                         NOTES TUI                                        |
|              A Terminal-Based Note Taking Application                    |
|                                                                          |
|                Built with ASCII Driven Development                       |
+==========================================================================+
```

## 1. Requirements

### User Stories

```
+===========================================================================+
|                           USER STORY MAP                                  |
+===========================================================================+
|                                                                           |
|  ACTIVITIES:   [ Manage Notes ]    [ Organize ]    [ Search ]            |
|                      |                  |              |                  |
+----------------------|------------------|--------------|------------------+
|                      |                  |              |                  |
|  USER TASKS:         v                  v              v                  |
|                +-----------+     +-----------+   +-----------+            |
|                | Create    |     | Create    |   | Search    |            |
|                | Note      |     | Notebook  |   | Notes     |            |
|                +-----------+     +-----------+   +-----------+            |
|                      |                  |              |                  |
|                +-----------+     +-----------+   +-----------+            |
|                | Edit      |     | Move Note |   | Filter by |            |
|                | Note      |     | to NB     |   | Notebook  |            |
|                +-----------+     +-----------+   +-----------+            |
|                      |                  |                                 |
|                +-----------+     +-----------+                            |
|                | Delete    |     | Rename    |                            |
|                | Note      |     | Notebook  |                            |
|                +-----------+     +-----------+                            |
|                      |                                                    |
|                +-----------+                                              |
|                | View      |                                              |
|                | Note      |                                              |
|                +-----------+                                              |
|                                                                           |
+===========================================================================+
```

### Requirements Matrix

```
+------+---------------------------+----------+--------+
| ID   | Requirement               | Priority | Status |
+------+---------------------------+----------+--------+
| R001 | Create new notes          | HIGH     | [TODO] |
| R002 | Edit existing notes       | HIGH     | [TODO] |
| R003 | Delete notes              | HIGH     | [TODO] |
| R004 | List all notes            | HIGH     | [TODO] |
| R005 | Search notes by title     | MEDIUM   | [TODO] |
| R006 | Search notes by content   | MEDIUM   | [TODO] |
| R007 | Organize notes in folders | LOW      | [TODO] |
| R008 | Keyboard navigation       | HIGH     | [TODO] |
| R009 | Persistent storage        | HIGH     | [TODO] |
| R010 | Syntax highlighting       | LOW      | [TODO] |
+------+---------------------------+----------+--------+
```

## 2. Architecture

### System Overview

```
+===========================================================================+
|                         SYSTEM ARCHITECTURE                               |
+===========================================================================+

    +-------------------------------------------------------------------+
    |                        PRESENTATION LAYER                          |
    |                                                                    |
    |  +------------------+  +------------------+  +------------------+  |
    |  |   List View      |  |   Editor View    |  |   Search View    |  |
    |  +------------------+  +------------------+  +------------------+  |
    |           |                    |                    |             |
    +-----------+--------------------+--------------------+-------------+
                |                    |                    |
                v                    v                    v
    +-------------------------------------------------------------------+
    |                         TUI ENGINE                                 |
    |                                                                    |
    |  +------------------+  +------------------+  +------------------+  |
    |  |   Screen         |  |   Input Handler  |  |   Renderer       |  |
    |  +------------------+  +------------------+  +------------------+  |
    +-------------------------------------------------------------------+
                                    |
                                    v
    +-------------------------------------------------------------------+
    |                       APPLICATION LAYER                            |
    |                                                                    |
    |  +------------------+  +------------------+  +------------------+  |
    |  |   NoteService    |  |   SearchService  |  |   AppState       |  |
    |  +------------------+  +------------------+  +------------------+  |
    +-------------------------------------------------------------------+
                                    |
                                    v
    +-------------------------------------------------------------------+
    |                         DATA LAYER                                 |
    |                                                                    |
    |  +------------------+  +------------------+                        |
    |  |   NoteRepository |  |   Storage (JSON) |                        |
    |  +------------------+  +------------------+                        |
    +-------------------------------------------------------------------+
```

### Component Interaction

```
    User Input          TUI Engine           App Logic            Storage
        |                   |                    |                   |
        | keypress          |                    |                   |
        |------------------>|                    |                   |
        |                   | handle_input()     |                   |
        |                   |------------------->|                   |
        |                   |                    | load/save         |
        |                   |                    |------------------>|
        |                   |                    |                   |
        |                   |                    |<------------------|
        |                   |<-------------------|                   |
        |                   |                    |                   |
        |                   | render()           |                   |
        |<------------------|                    |                   |
        |                   |                    |                   |
```

## 3. Data Model

### Entity Relationship

```
+------------------+           +------------------+
|      NOTE        |           |    NOTEBOOK      |
+------------------+           +------------------+
| PK id: string    |     +---->| PK id: string    |
|    title: string |     |     |    name: string  |
|    content: text |     |     |    created_at    |
|    created_at    |     |     |    updated_at    |
|    updated_at    |     |     +------------------+
| FK notebook_id   |-----+
+------------------+

    Note : Notebook = N : 1
    (A note belongs to one notebook)
    (A notebook contains many notes)
```

### JSON Storage Schema

```
{
  "notebooks": [
    {
      "id": "nb_001",
      "name": "Default",
      "created_at": "2026-01-14T10:00:00Z",
      "updated_at": "2026-01-14T10:00:00Z"
    }
  ],
  "notes": [
    {
      "id": "note_001",
      "notebook_id": "nb_001",
      "title": "My First Note",
      "content": "Hello, world!",
      "created_at": "2026-01-14T10:00:00Z",
      "updated_at": "2026-01-14T10:00:00Z"
    }
  ]
}
```

## 4. User Interface Design

### Main Layout

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
|  |   Ideas      (2)|     |  |   Project Ideas              2026-01-11    |
|  +-----------------+     |  |   Code Snippets              2026-01-10    |
|                          |  +---------------------------------------------+
|  [N] New Notebook        |                                                |
|                          |  [n] New  [e] Edit  [d] Delete  [/] Search     |
+--------------------------+------------------------------------------------+
|                                                                           |
|  Status: 18 notes | Selected: My First Note | Press ? for help           |
|                                                                           |
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
|  Features I want to implement:                                            |
|  - Create and edit notes                                                  |
|  - Organize in notebooks                                                  |
|  - Search functionality                                                   |
|  - Keyboard navigation                                                    |
|                                                                           |
|  _                                                                        |
|                                                                           |
|                                                                           |
|                                                                           |
+===========================================================================+
|  Line 12, Col 1 | Modified | Notebook: Default                           |
+===========================================================================+
```

### Search View

```
+===========================================================================+
|  SEARCH                                                       [Esc] Back |
+===========================================================================+
|                                                                           |
|  Search: meeting_                                                         |
|  -----------------------------------------------------------------------  |
|                                                                           |
|  Results (3 matches):                                                     |
|  +---------------------------------------------------------------------+  |
|  | > Meeting Notes                                         [Default]  |  |
|  |   "Discussed project timeline in the meeting..."                   |  |
|  +---------------------------------------------------------------------+  |
|  |   Weekly Meeting Agenda                                 [Work]     |  |
|  |   "Topics for the weekly meeting: 1. Status..."                    |  |
|  +---------------------------------------------------------------------+  |
|  |   Meeting Room Booking                                  [Personal] |  |
|  |   "Remember to book meeting room for Friday..."                    |  |
|  +---------------------------------------------------------------------+  |
|                                                                           |
+===========================================================================+
|  [Enter] Open  [Tab] Next  [Esc] Cancel                                  |
+===========================================================================+
```

### Help Dialog

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
|  r             Rename notebook                |
|                                               |
|  GENERAL                                      |
|  ------------------------------------------- |
|  ?             Show this help                 |
|  q / Q         Quit application               |
|  Esc           Cancel / Go back               |
|                                               |
|              [Press any key to close]         |
+-----------------------------------------------+
```

## 5. State Machine

### Application States

```
                         APPLICATION STATE MACHINE

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
        +----------+
        |  SAVING  |
        +----+-----+
             |
             | complete
             v
        [Return to LIST VIEW]


    QUIT FLOW (from any state):

        [ANY STATE] --'q'--> [CONFIRM] --'y'--> [EXIT]
                                  |
                                  | 'n'
                                  v
                             [RETURN]
```

## 6. Project Structure

```
notes-tui/
|
+-- src/
|   +-- main.py              # Application entry point
|   +-- app.py               # Main application class
|   |
|   +-- models/
|   |   +-- __init__.py
|   |   +-- note.py          # Note data model
|   |   +-- notebook.py      # Notebook data model
|   |
|   +-- services/
|   |   +-- __init__.py
|   |   +-- note_service.py  # Note business logic
|   |   +-- search_service.py # Search functionality
|   |
|   +-- storage/
|   |   +-- __init__.py
|   |   +-- repository.py    # Data persistence
|   |
|   +-- tui/
|   |   +-- __init__.py
|   |   +-- screen.py        # Terminal screen handling
|   |   +-- renderer.py      # UI rendering
|   |   +-- input_handler.py # Keyboard input
|   |   +-- components/
|   |       +-- __init__.py
|   |       +-- list_view.py
|   |       +-- editor_view.py
|   |       +-- search_view.py
|   |       +-- help_dialog.py
|   |
|   +-- utils/
|       +-- __init__.py
|       +-- helpers.py
|
+-- data/
|   +-- notes.json           # Persistent storage
|
+-- tests/
|   +-- test_models.py
|   +-- test_services.py
|   +-- test_storage.py
|
+-- DESIGN.md                # This document
+-- README.md
+-- requirements.txt
```

## 7. Implementation Plan

```
+==================+==================+==================+==================+
|     PHASE 1      |     PHASE 2      |     PHASE 3      |     PHASE 4      |
|   Foundation     |    Core TUI      |    Features      |    Polish        |
+==================+==================+==================+==================+
|                  |                  |                  |                  |
| [x] Data models  | [ ] Screen mgmt  | [ ] Search       | [ ] Error handle |
| [x] Storage      | [ ] List view    | [ ] Notebooks    | [ ] Help system  |
| [x] Repository   | [ ] Editor view  | [ ] Move notes   | [ ] Confirmation |
|                  | [ ] Input handle | [ ] Rename       | [ ] Status bar   |
|                  |                  |                  |                  |
+------------------+------------------+------------------+------------------+
```

---

*Design document created following ASCII Driven Development principles.*
