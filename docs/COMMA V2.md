# Comma V2
## Product & Technical Specification

**Status:** Draft  
**Version:** 2.0  
**Purpose:** Source of truth for the Comma V2 redesign

---

# 1. Vision

Comma is an always-visible desktop note system designed to keep important information present without becoming another application window that needs to be opened.

The fundamental idea is:

> **Your notes should live on your desktop, not inside an app.**

Comma V2 evolves the existing always-on-top task manager into a collection of lightweight, persistent desktop notes.

Each note exists independently, can be positioned around the desktop, can remain partially hidden at the screen edge, and can be quickly expanded when needed.

The application should feel like a **desktop utility**, not a conventional productivity application.

---

# 2. Problem

Traditional note-taking applications require the user to:

1. Open the application.
2. Find the relevant note.
3. Read or edit it.
4. Close or minimize the application.

This creates friction for information that needs to remain visible.

Comma solves this by keeping notes continuously available while minimizing the amount of desktop space they consume.

The desired interaction is:

```text
Need information
      ↓
See note immediately
      ↓
Interact with note
      ↓
Note returns to background/edge
```

No application switching should be necessary.

---

# 3. Product Principles

Comma V2 follows these principles.

## 3.1 Always available

A note should be accessible without opening a main application window.

## 3.2 Minimal visual footprint

When not actively being used, notes should consume very little screen space.

## 3.3 Fast interaction

Expanding, editing, moving and collapsing a note should require minimal interaction.

## 3.4 Persistent state

A note should remember its content, appearance, position and relevant UI state between launches.

## 3.5 Desktop-native behavior

Comma should behave like a native desktop utility rather than a web application disguised as one.

## 3.6 No unnecessary complexity

The interface should remain focused on notes.

Features should only be added when they support the core experience.

---

# 4. Current Comma Baseline

The current Comma implementation is a Python/PyQt5 desktop task manager.

Current capabilities include:

- Always-on-top application window
- Task creation
- Task editing
- Task deletion
- Priority levels
- Categories
- Light/dark themes
- Task statistics
- JSON persistence
- JSON import/export
- Desktop builds for Windows, macOS and Linux

The current application is centered around a single primary window.

Comma V2 changes the interaction model from:

```text
Application
    └── Task list
          ├── Task
          ├── Task
          └── Task
```

to:

```text
Application Controller
    ├── Note
    ├── Note
    ├── Note
    └── Note
```

Each note becomes an independent desktop object.

---

# 5. Core Concept

A **Note** is the fundamental unit of Comma.

A note contains:

```text
Note
├── Identity
├── Title
├── Content
├── Appearance
├── Position
├── Dock state
└── Lifecycle state
```

Example:

```json
{
  "id": "note-001",
  "title": "Groceries",
  "content": "Apple\nPineapple\nGinger",
  "color": "...",
  "position": {
    "x": 1600,
    "y": 300
  },
  "edge": "right",
  "docked": true,
  "archived": false
}
```

The exact schema will be finalized in `data-model.md`.

---

# 6. Note Lifecycle

A note can move through the following states:

```text
                 ┌───────────┐
                 │   Created │
                 └─────┬─────┘
                       ↓
                 ┌───────────┐
                 │   Active  │
                 └─────┬─────┘
                       │
              ┌────────┴────────┐
              ↓                 ↓
          Docked             Expanded
              ↑                 │
              └────────┬────────┘
                       │
                       ↓
                  Archived
```

A note may move between docked and expanded states repeatedly.

Archiving removes it from the active desktop without permanently deleting its content.

---

# 7. Desktop Presence

The defining feature of Comma V2 is persistent desktop presence.

A note may be positioned at an edge of the screen.

Initial supported edge:

```text
RIGHT
```

The architecture should allow future support for:

```text
LEFT
TOP
BOTTOM
```

without requiring a redesign of the note system.

---

# 8. Docked State

A docked note is partially hidden at the edge of the screen.

Example:

```text
                         SCREEN

┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│                                      ┌──────┤
│                                      │ Note │
│                                      └──────┤
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

Only a small portion of the note remains visible.

The docked state should:

- consume minimal screen space
- remain visible
- remain accessible
- preserve the note's position
- provide an obvious interaction target

---

# 9. Expanded State

When the user interacts with a docked note, it expands onto the desktop.

Example:

```text
┌──────────────────────────────────────────────┐
│                                              │
│                         ┌──────────────────┐ │
│                         │ Groceries    ··· │ │
│                         ├──────────────────┤ │
│                         │ Apple            │ │
│                         │ Pineapple        │ │
│                         │ Ginger           │ │
│                         │                  │ │
│                         └──────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

The expanded note:

- becomes fully visible
- can be edited
- can be dragged
- remains above normal desktop applications where appropriate
- remains associated with its original note identity

---

# 10. Expand / Collapse Interaction

The transition between docked and expanded states should be animated.

Expected behavior:

```text
DOCKED
   ↓
interaction
   ↓
EXPANDING
   ↓
EXPANDED
```

and:

```text
EXPANDED
   ↓
mouse leaves / user dismisses
   ↓
COLLAPSING
   ↓
DOCKED
```

The animation should be short and unobtrusive.

The animation exists to communicate spatial movement, not to become a visual effect by itself.

---

# 11. Hover Behavior

Hovering over a docked note should initiate its reveal.

However, the implementation must avoid accidental collapsing while the user moves the pointer from the edge into the expanded note.

The state machine should therefore distinguish:

```text
DOCKED
EXPANDING
EXPANDED
COLLAPSING
DRAGGING
```

A note must not collapse while:

- the cursor is inside the note
- the note is being dragged
- the user is actively editing it
- an interaction is in progress

---

# 12. Editing

An expanded note should be directly editable.

The user should not need to enter a separate "edit mode" for basic text editing.

Example:

```text
┌──────────────────────────┐
│ Groceries                │
├──────────────────────────┤
│ Apple                    │
│ Pineapple                │
│ Ginger                   │
│                          │
│                          │
└──────────────────────────┘
```

Changes should be persisted automatically or through a lightweight save mechanism.

The user should never lose note content because a note was collapsed.

---

# 13. Dragging

Expanded notes must be draggable.

Dragging should allow the user to reposition a note freely on the desktop.

The system should track:

```text
x
y
```

coordinates.

When a note is moved close enough to a supported screen edge, it may snap to that edge.

Example:

```text
Free position
      ↓
drag toward edge
      ↓
edge threshold reached
      ↓
snap
      ↓
docked
```

The exact snap threshold will be defined during implementation.

---

# 14. Multiple Notes

Comma must support multiple independent notes.

Example:

```text
RIGHT EDGE

┌──────┐
│ Work │
├──────┤
│ Ideas│
├──────┤
│ Todo │
├──────┤
│ Read │
└──────┘
```

Each note must have:

- independent content
- independent position
- independent appearance
- independent state

The application controller is responsible for managing all active note windows.

---

# 15. Note Stacking

Docked notes should be arranged so they do not overlap unnecessarily.

The manager should calculate their positions based on:

- screen dimensions
- note dimensions
- edge
- ordering
- spacing

The exact stacking algorithm belongs to the architecture phase.

The first implementation should prioritize predictable behavior over sophisticated collision management.

---

# 16. Note Appearance

Notes should have a visually distinct but restrained appearance.

A note should communicate:

- its identity
- its title
- its content
- its active/inactive state

Notes may use different colors.

Color should be stored as part of note state.

Example:

```text
Yellow → Ideas
Blue   → Work
Green  → Personal
Red    → Urgent
```

The exact palette will be defined separately.

---

# 17. Note Controls

The expanded note may provide lightweight controls for actions such as:

```text
Edit
Archive
Export
Delete
```

Controls should remain visually secondary to the note content.

The primary interaction should always be the note itself.

---

# 18. Archive

Archiving is a non-destructive lifecycle operation.

When a note is archived:

```text
Active desktop
      ↓
Archive
      ↓
Removed from desktop
      ↓
Stored in persistent data
```

Archived notes should remain recoverable.

Archive and permanent deletion must be treated as separate operations.

---

# 19. Export

Users should be able to export notes for portability.

The first supported export format should be:

```text
JSON
```

Future formats may include:

```text
TXT
Markdown
```

Export functionality must not affect the original note.

---

# 20. Persistence

Comma must restore the user's workspace after restarting the application.

At minimum, persistent state must include:

```text
Note ID
Title
Content
Color
Position
Dock edge
Dock state
Archive state
```

Potential future fields:

```text
Created timestamp
Updated timestamp
Size
Dimensions
Tags
Pinned state
```

Persistence implementation should remain local-first.

No cloud service is required for V2.

---

# 21. Application Controller

Comma V2 should have one central controller responsible for:

- loading notes
- creating notes
- destroying note windows
- tracking active notes
- saving state
- restoring state
- managing dock positions
- handling application lifecycle

Conceptually:

```text
                 QApplication
                       │
                       ▼
                 NoteManager
              ┌────────┼────────┐
              ↓        ↓        ↓
           Note A    Note B    Note C
```

Individual note windows should not own global application state.

---

# 22. Separation of Concerns

The implementation should maintain a clean separation between:

### Model

Stores note data.

```text
Note
```

### Manager / Controller

Handles application-wide note management.

```text
NoteManager
```

### View

Displays and interacts with the note.

```text
NoteWindow
```

### Persistence

Loads and saves models.

```text
Storage / Repository
```

This prevents UI behavior from becoming tightly coupled to JSON storage.

---

# 23. Proposed Architecture

```text
┌───────────────────────────────┐
│          QApplication         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          AppController        │
│                               │
│  - lifecycle                  │
│  - shortcuts                  │
│  - application state          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          NoteManager          │
│                               │
│  - create                     │
│  - remove                     │
│  - archive                    │
│  - restore                    │
│  - arrange                    │
└───────┬───────────┬───────────┘
        │           │
        ▼           ▼
   ┌─────────┐ ┌─────────┐
   │ Note    │ │ Note    │
   │ Model   │ │ Model   │
   └────┬────┘ └────┬────┘
        │            │
        ▼            ▼
   ┌─────────┐ ┌─────────┐
   │ Note    │ │ Note    │
   │ Window  │ │ Window  │
   └─────────┘ └─────────┘

                │
                ▼
       ┌─────────────────┐
       │    Storage      │
       │                 │
       │      JSON       │
       └─────────────────┘
```

---

# 24. Platform Requirements

Comma currently targets:

- Windows
- macOS
- Linux

V2 should preserve this goal.

Platform-specific behavior may be required for:

- window flags
- always-on-top behavior
- screen geometry
- taskbar/dock interaction
- multi-monitor support
- window activation
- system tray behavior

Platform-specific logic should be isolated rather than scattered throughout the UI code.

---

# 25. Multi-Monitor Support

The architecture should account for multiple displays.

A note belongs to a particular desktop coordinate space.

The system should avoid restoring a note to a position that no longer exists because a monitor was disconnected.

If necessary:

```text
Saved position
      ↓
Monitor unavailable
      ↓
Find valid screen
      ↓
Clamp/reposition note
```

Multi-monitor optimization is not a V2 Phase 1 requirement but the architecture must not prevent it.

---

# 26. Keyboard Interaction

Keyboard shortcuts should remain an important part of Comma.

Initial shortcuts should include equivalents for:

```text
Create note
Close/collapse note
Archive note
Delete note
```

Exact shortcuts will be defined in the interaction specification.

Keyboard behavior should never conflict with normal text editing.

---

# 27. Application Entry Point

Comma should remain a single desktop application from the user's perspective.

The presence of multiple windows must not mean multiple application instances.

Conceptually:

```text
One Comma process
       │
       ├── Note A
       ├── Note B
       ├── Note C
       └── Controller
```

Launching Comma again should ideally detect the existing instance rather than creating an uncontrolled second workspace.

Single-instance behavior is a future architectural requirement if not already implemented.

---

# 28. Non-Goals for V2

The following are explicitly outside the initial V2 scope:

- Cloud synchronization
- User accounts
- Collaboration
- Real-time multi-user editing
- AI note generation
- Mobile application
- Browser extension
- Complex rich-text editor
- Online database
- Social features
- Calendar integration
- Reminder notification system
- Complex tagging/search infrastructure

These may become future projects, but they should not contaminate the core V2 implementation.

---

# 29. Phase Roadmap

V2 will be developed in controlled phases.

## Phase 0: Documentation & Architecture

Establish:

- product specification
- interaction specification
- architecture
- data model
- phase contracts

**No feature implementation.**

---

## Phase 1: Independent Note Windows

Goal:

Replace the single task-manager window with independently managed note windows.

Deliver:

- Note model
- NoteWindow
- NoteManager
- basic note creation
- basic note editing
- always-on-top behavior

No docking animation yet.

---

## Phase 2: Docking System

Goal:

Allow notes to attach to the screen edge.

Deliver:

- docked state
- expanded state
- edge positioning
- docking/undocking logic

---

## Phase 3: Reveal & Animation

Goal:

Reproduce the reference video's interaction.

Deliver:

- hover detection
- animated expansion
- animated collapse
- interaction-safe state transitions

---

## Phase 4: Dragging & Snapping

Goal:

Allow notes to be freely positioned.

Deliver:

- drag handling
- position tracking
- edge detection
- snapping
- persistent coordinates

---

## Phase 5: Multiple Notes

Goal:

Make the desktop workspace behave correctly with multiple notes.

Deliver:

- multiple active notes
- stacking
- spacing
- ordering
- collision avoidance

---

## Phase 6: Persistence

Goal:

Restore the complete workspace after restart.

Deliver:

- note serialization
- automatic saving
- restoration
- migration from existing Comma data where practical

---

## Phase 7: Archive & Export

Goal:

Provide note lifecycle management.

Deliver:

- archive
- restore
- permanent delete
- JSON export
- future export abstraction

---

## Phase 8: Visual Polish

Goal:

Match the intended Comma V2 visual language.

Deliver:

- typography
- colors
- spacing
- shadows
- borders
- animations
- dark/light themes
- interaction feedback

---

## Phase 9: Testing & Packaging

Goal:

Make Comma V2 stable enough for real daily use.

Deliver:

- functional tests
- persistence tests
- interaction tests
- platform checks
- packaging
- regression testing
- documentation updates

---

# 30. Definition of V2

Comma V2 is considered complete when a user can:

1. Launch Comma.
2. Create multiple notes.
3. See those notes persistently on the desktop.
4. Allow notes to remain docked at the screen edge.
5. Reveal a note through interaction.
6. Edit its content directly.
7. Drag it around the desktop.
8. Dock it again.
9. Close and reopen Comma.
10. Find the notes exactly where they were left.
11. Archive notes without losing them.
12. Export notes.
13. Use the system without needing a conventional central application window.

---

# 31. Acceptance Criteria

The implementation must satisfy the following high-level criteria.

### Desktop Presence

- Notes remain visible when the user is working in other applications.
- Notes remain above normal windows where configured.

### Interaction

- Docked notes can be revealed reliably.
- Expanded notes do not accidentally collapse during interaction.
- Notes can be edited without entering a separate workflow.

### Positioning

- Notes can be dragged.
- Notes can be docked to supported edges.
- Positions survive application restart.

### Persistence

- Content survives restart.
- Appearance survives restart.
- Position survives restart.
- Archive state survives restart.

### Multiple Notes

- Multiple notes can coexist.
- Notes do not unintentionally overlap.
- Each note behaves independently.

### Reliability

- Closing one note does not terminate Comma.
- A corrupted/missing persistence file does not prevent application startup.
- Invalid saved positions are handled safely.

---

# 32. Development Rules

During V2 implementation:

### Rule 1
Do not implement functionality belonging to a future phase unless required by the current architecture.

### Rule 2
Every phase must have a defined acceptance test.

### Rule 3
Do not rewrite working functionality without a documented reason.

### Rule 4
Prefer small, reversible changes.

### Rule 5
Keep model, controller, view and persistence responsibilities separate.

### Rule 6
Update documentation when architecture changes.

### Rule 7
If implementation reveals a requirement missing from this specification, stop and update the specification before expanding scope.

---

# 33. Source of Truth

The documentation hierarchy is:

```text
COMMA_V2.md
      │
      ├── architecture.md
      ├── interaction-spec.md
      ├── data-model.md
      │
      └── phases/
            ├── phase-01-...
            ├── phase-02-...
            └── ...
```

`COMMA_V2.md` defines **what Comma V2 is**.

`architecture.md` defines **how it is structured**.

`interaction-spec.md` defines **how it behaves**.

`data-model.md` defines **what data exists**.

Individual phase documents define **what we are allowed to build at each stage**.

---

# 34. Final Product Definition

> **Comma is a persistent desktop note system that keeps information visible, accessible and lightweight.**

The application should disappear into the desktop when it is not needed and become immediately useful when it is.

The goal is not to build another note-taking application.

The goal is to make **remembering things require almost no interaction at all.**