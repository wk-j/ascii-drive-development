# ASCII Driven Development

```
+===========================================================================+
|                                                                           |
|     █████╗ ███████╗ ██████╗██╗██╗                                        |
|    ██╔══██╗██╔════╝██╔════╝██║██║                                        |
|    ███████║███████╗██║     ██║██║                                        |
|    ██╔══██║╚════██║██║     ██║██║                                        |
|    ██║  ██║███████║╚██████╗██║██║                                        |
|    ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝                                        |
|                                                                           |
|    ██████╗ ██████╗ ██╗██╗   ██╗███████╗███╗   ██╗                        |
|    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝████╗  ██║                        |
|    ██║  ██║██████╔╝██║██║   ██║█████╗  ██╔██╗ ██║                        |
|    ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║                        |
|    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║ ╚████║                        |
|    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝                        |
|                                                                           |
|    ██████╗ ███████╗██╗   ██╗                                             |
|    ██╔══██╗██╔════╝██║   ██║                                             |
|    ██║  ██║█████╗  ██║   ██║                                             |
|    ██║  ██║██╔══╝  ╚██╗ ██╔╝                                             |
|    ██████╔╝███████╗ ╚████╔╝                                              |
|    ╚═════╝ ╚══════╝  ╚═══╝                                               |
|                                                                           |
|        "If you can't express it in ASCII, you don't understand it"       |
|                                                                           |
+===========================================================================+
```

## What is ASCII Driven Development?

**ASCII Driven Development (ADD)** is a software development methodology that emphasizes using plain-text ASCII diagrams and documentation throughout the entire development lifecycle.

### Core Principles

```
+-------------------+     +-------------------+     +-------------------+
|    UNIVERSAL      |     |   VERSION         |     |   LIGHTWEIGHT     |
|                   |     |   CONTROL         |     |                   |
| • Works anywhere  |     | • Git-friendly    |     | • No special      |
| • No special      |     | • Diff-able       |     |   tools needed    |
|   software        |     | • Merge-able      |     | • Fast to create  |
| • Copy/paste      |     | • History tracked |     | • Easy to modify  |
+-------------------+     +-------------------+     +-------------------+
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                    +---------------------------+
                    |   BETTER COMMUNICATION    |
                    |                           |
                    | • Clear mental models     |
                    | • Shared understanding    |
                    | • Documentation as code   |
                    +---------------------------+
```

### Why ASCII?

| Benefit | Description |
|---------|-------------|
| **Universal** | Works in any editor, terminal, or platform |
| **Version Control** | Perfect git diffs, easy merging |
| **Lightweight** | No binary files, no special software |
| **Durable** | Plain text never becomes obsolete |
| **Accessible** | Anyone can read and edit |

## Repository Contents

```
ascii-driven-development/
│
├── ASCII-DRIVEN-DEVELOPMENT.md    # 📖 Complete ADD methodology guide
│                                   #    Covers the full software lifecycle
│
├── notes-tui/                      # 💻 Example TUI application
│   ├── DESIGN.md                  #    Design document (ADD style)
│   ├── README.md                  #    Application documentation
│   └── src/                       #    Python source code
│
└── README.md                      # 📄 This file
```

## Quick Start

### 1. Read the Methodology

Start with the comprehensive guide covering all phases of software development:

```bash
cat ASCII-DRIVEN-DEVELOPMENT.md
```

This document includes ASCII diagram examples for:
- Requirements & Planning
- System Design & Architecture
- Implementation
- Testing
- Deployment & Operations
- Maintenance & Evolution

### 2. Try the Example Application

The `notes-tui` directory contains a fully-functional terminal note-taking app built using ADD principles:

```bash
cd notes-tui
python -m src.main
```

Features:
- 󰎚 Create, edit, delete notes
- 📁 Organize in notebooks
- 🔍 Search functionality
- ⌨️ Vim-style navigation
- 🎨 Nerd Font icons (with fallback)

## ADD Diagram Examples

### Architecture Diagram

```
                              ┌─────────────┐
                              │   CLIENT    │
                              └──────┬──────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │     LOAD BALANCER      │
                        └────────────────────────┘
                           /         │         \
                          ▼          ▼          ▼
                    ┌────────┐ ┌────────┐ ┌────────┐
                    │ App 1  │ │ App 2  │ │ App 3  │
                    └────┬───┘ └────┬───┘ └────┬───┘
                         └──────────┼──────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │          DATABASE             │
                    └───────────────────────────────┘
```

### Sequence Diagram

```
    User            Frontend         Backend          Database
      │                │                │                │
      │  1. Request    │                │                │
      │───────────────>│                │                │
      │                │  2. API Call   │                │
      │                │───────────────>│                │
      │                │                │  3. Query      │
      │                │                │───────────────>│
      │                │                │                │
      │                │                │  4. Results    │
      │                │                │<───────────────│
      │                │  5. Response   │                │
      │                │<───────────────│                │
      │  6. Display    │                │                │
      │<───────────────│                │                │
```

### State Machine

```
                    ┌─────────┐
                    │  IDLE   │
                    └────┬────┘
                         │ start
                         ▼
                    ┌─────────┐
        ┌──────────│ RUNNING │──────────┐
        │ pause    └────┬────┘  error   │
        ▼               │               ▼
   ┌─────────┐          │          ┌─────────┐
   │ PAUSED  │          │ complete │  ERROR  │
   └────┬────┘          │          └────┬────┘
        │ resume        ▼               │ retry
        │          ┌─────────┐          │
        └─────────>│  DONE   │<─────────┘
                   └─────────┘
```

### ERD (Entity Relationship)

```
┌──────────────────┐       ┌──────────────────┐
│      USER        │       │      ORDER       │
├──────────────────┤       ├──────────────────┤
│ PK id            │       │ PK id            │
│    name          │───┐   │ FK user_id       │──┐
│    email         │   │   │    total         │  │
│    created_at    │   │   │    status        │  │
└──────────────────┘   │   │    created_at    │  │
                       │   └──────────────────┘  │
                       │                         │
                       └─────────────────────────┘
                              1 : N
```

## Tools & Resources

### Creating ASCII Diagrams

- **Text editors**: Any editor works (VS Code, Vim, Emacs)
- **Online tools**: [ASCIIFlow](https://asciiflow.com), [Monodraw](https://monodraw.helftone.com)
- **CLI tools**: `boxes`, `figlet`, `toilet`

### Box Drawing Characters

```
Single line:  ┌─┬─┐    Double line:  ╔═╦═╗
              │ │ │                  ║ ║ ║
              ├─┼─┤                  ╠═╬═╣
              │ │ │                  ║ ║ ║
              └─┴─┘                  ╚═╩═╝

Arrows:  → ← ↑ ↓ ↔ ↕    Corners:  ╭─╮
                                  │ │
         ▶ ◀ ▲ ▼                  ╰─╯

Bullets: • ○ ◆ ◇ ■ □ ★ ☆
```

## Contributing

Contributions are welcome! When contributing:

1. Use ASCII diagrams in your documentation
2. Keep diagrams simple and readable
3. Test that diagrams display correctly in monospace fonts
4. Follow existing style conventions

## License

MIT License - See [LICENSE](LICENSE) for details.

---

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   "The best documentation is the one that gets maintained."    │
│                                                                 │
│   ASCII diagrams are easy to create, easy to update, and       │
│   impossible to lose in a proprietary format.                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
