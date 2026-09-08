# Comma V2

## Architecture Specification

**Status:** Draft
**Version:** 2.0
**Parent Document:** `COMMA_V2.md`

---

# 1. Purpose

This document defines the technical architecture for Comma V2.

It answers:

* What components exist?
* What does each component own?
* How do components communicate?
* Where does state live?
* How does a user action travel through the system?
* What boundaries must remain intact during implementation?

This document does **not** define visual styling in detail.

---

# 2. Architectural Direction

Comma V2 will remain a **native Python desktop application using PyQt5**.

The architecture will evolve from the current monolithic application toward a small layered desktop system.

The target architecture is:

```text
                    ┌──────────────────┐
                    │    Application   │
                    │     Runtime      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  AppController   │
                    └────────┬─────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │ NoteManager  │      │   Storage    │
          └──────┬───────┘      └──────┬───────┘
                 │                     │
                 │                     │
        ┌────────┼────────┐            │
        ▼        ▼        ▼            │
      Note     Note     Note            │
        │        │        │             │
        ▼        ▼        ▼             │
      View     View     View            │
        │        │        │             │
        └────────┴────────┴─────────────┘
```

The important rule is:

> **The UI displays state. It should not become the owner of application state.**

---

# 3. Architectural Layers

Comma will contain four primary layers.

```text
┌───────────────────────────────┐
│ Presentation                   │
│ NoteWindow / UI components     │
├───────────────────────────────┤
│ Application                    │
│ AppController / NoteManager    │
├───────────────────────────────┤
│ Domain                         │
│ Note / NoteState / enums       │
├───────────────────────────────┤
│ Infrastructure                 │
│ JSON storage / platform logic  │
└───────────────────────────────┘
```

Each layer has a defined responsibility.

---

# 4. Domain Layer

The domain layer contains concepts that describe Comma itself.

Primary object:

```python
Note
```

A note should contain data, not PyQt widgets.

Example:

```python
@dataclass
class Note:
    id: str
    title: str
    content: str
    color: str
    x: int
    y: int
    width: int
    height: int
    edge: str
    state: str
    archived: bool
```

The exact model will be defined in `data-model.md`.

The domain model must remain usable without creating a GUI window.

This is important because it allows:

* persistence tests
* model tests
* migrations
* future alternate interfaces
* predictable application state

---

# 5. Note State

The UI should not infer state from random widget properties.

Instead, note state should be explicit.

Initial state machine:

```text
             ┌─────────┐
             │ DOCKED  │
             └────┬────┘
                  │
             hover/click
                  │
                  ▼
             ┌─────────┐
             │EXPANDING│
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
        ┌────│EXPANDED │────┐
        │    └─────────┘    │
        │                   │
      drag              mouse leave
        │                   │
        ▼                   ▼
   ┌─────────┐        ┌───────────┐
   │ DRAGGING│        │ COLLAPSING│
   └────┬────┘        └─────┬─────┘
        │                   │
        │                   ▼
        │              ┌─────────┐
        └─────────────►│ DOCKED  │
                       └─────────┘
```

Potential future states:

```text
CREATING
ARCHIVED
DELETING
```

but they should not be introduced into the interaction state machine unless required.

---

# 6. Presentation Layer

The primary visual object is:

```python
NoteWindow(QWidget)
```

A `NoteWindow` is responsible for:

* rendering a note
* receiving mouse events
* receiving keyboard events
* editing note content
* displaying controls
* performing visual transitions
* reporting user actions

It must **not** be responsible for:

* loading JSON
* deciding which notes exist
* globally arranging every note
* managing the application lifecycle
* directly modifying unrelated notes

---

# 7. NoteWindow Responsibilities

Conceptually:

```text
NoteWindow
│
├── Header
│   ├── Title
│   └── Menu
│
├── ContentEditor
│
├── Footer
│   ├── Color / metadata
│   ├── Archive
│   └── Export
│
└── InteractionController
    ├── Hover
    ├── Drag
    ├── Dock
    └── Animation
```

The exact widget tree may differ during implementation.

The architectural responsibility should remain the same.

---

# 8. Application Layer

The application layer coordinates the system.

Two primary components:

```text
AppController
NoteManager
```

---

# 9. AppController

`AppController` owns application-wide lifecycle.

Responsibilities:

* create the QApplication
* initialize storage
* load workspace
* initialize NoteManager
* register global application behavior
* handle application shutdown
* trigger final persistence
* coordinate future system-tray behavior

Conceptually:

```python
class AppController:
    storage
    note_manager

    def start():
        load_workspace()
        restore_notes()

    def shutdown():
        save_workspace()
```

`AppController` should not know how a note is visually rendered.

---

# 10. NoteManager

`NoteManager` owns the active note collection.

Responsibilities:

* create notes
* register notes
* remove notes
* archive notes
* restore notes
* create/destroy NoteWindow instances
* coordinate note arrangement
* coordinate docking
* expose active note state

Conceptually:

```python
class NoteManager:

    notes: dict[str, Note]
    windows: dict[str, NoteWindow]

    def create_note(...)
    def open_note(note_id)
    def close_note(note_id)
    def archive_note(note_id)
    def delete_note(note_id)
```

The manager maintains the relationship:

```text
Note ID
   │
   ├── Note model
   │
   └── NoteWindow
```

---

# 11. Why Model and Window Are Separate

A common mistake would be:

```python
window.note.content
window.note.x
window.note.save()
window.note.archive()
```

with the widget effectively becoming the application's database.

We should instead use:

```text
User interaction
      ↓
NoteWindow
      ↓
event / command
      ↓
NoteManager
      ↓
Note model changes
      ↓
persistence
      ↓
NoteWindow updates
```

This keeps state ownership clear.

---

# 12. Communication Pattern

The system should use explicit events/signals.

Example:

```text
NoteWindow
    │
    │ content_changed
    ▼
NoteManager
    │
    │ update model
    ▼
Storage
```

Another:

```text
NoteWindow
    │
    │ drag_finished(x, y)
    ▼
NoteManager
    │
    │ update position
    ▼
Storage
```

PyQt signals are appropriate for UI-to-controller communication.

---

# 13. Storage Layer

Persistence should be isolated behind a storage interface.

Conceptually:

```python
class Storage:
    def load_workspace(self) -> Workspace:
        ...

    def save_workspace(self, workspace):
        ...
```

The initial implementation will use JSON.

The rest of the application should not care whether persistence is:

```text
JSON
SQLite
Cloud
```

This allows future evolution without rewriting the UI.

---

# 14. JSON Storage

The initial storage format remains local JSON.

Conceptually:

```text
data/
└── notes.json
```

Actual path should continue respecting the existing Comma configuration/platform conventions.

Storage responsibilities:

```text
Application
    ↓
Workspace
    ↓
Storage
    ↓
JSON
```

Storage should handle:

* file creation
* loading
* saving
* malformed data
* missing fields
* schema versioning
* migrations

---

# 15. Schema Versioning

V2 should introduce a schema version.

Example:

```json
{
    "schema_version": 2,
    "notes": []
}
```

This prevents future changes from breaking existing user data.

Migration flow:

```text
Old JSON
   ↓
Detect schema version
   ↓
Migration
   ↓
Current model
   ↓
Application
```

Migration should be isolated from UI code.

---

# 16. Workspace

A `Workspace` represents the persisted Comma state.

Conceptually:

```python
@dataclass
class Workspace:
    schema_version: int
    notes: list[Note]
    settings: Settings
```

This separates:

```text
Individual note
```

from:

```text
Entire Comma environment
```

---

# 17. Docking Architecture

Docking should not be implemented entirely inside `NoteWindow`.

We divide responsibility.

### NoteWindow

Knows:

```text
"I am being dragged."
"I am currently expanded."
"My geometry changed."
```

### DockManager

Knows:

```text
"Where should this note dock?"
"Which screen edge is nearest?"
"Where should this note be placed?"
"How should multiple notes be stacked?"
```

Architecture:

```text
NoteWindow
     │
     │ geometry event
     ▼
DockManager
     │
     ├── detect edge
     ├── calculate dock position
     └── calculate expanded position
```

---

# 18. DockManager

The initial API should conceptually resemble:

```python
class DockManager:

    def nearest_edge(position, screen):
        ...

    def dock(note, edge):
        ...

    def undock(note):
        ...

    def calculate_dock_geometry(note, edge):
        ...

    def arrange_notes(notes, edge):
        ...
```

This component becomes increasingly important when multiple notes are introduced.

---

# 19. Screen Geometry

The application must use Qt's screen abstraction rather than assuming one fixed resolution.

Conceptually:

```python
QApplication.screens()
```

and:

```python
screen.availableGeometry()
```

The distinction between:

```text
screen geometry
```

and:

```text
available desktop geometry
```

must be respected.

This prevents notes from being positioned beneath taskbars, docks or other reserved desktop areas where possible.

---

# 20. Animation Architecture

Animation is presentation logic.

The application should not modify the domain model repeatedly during an animation.

For example, expanding a note should conceptually be:

```text
Stored state:
DOCKED

Animation:
geometry A → geometry B

Completion:
EXPANDED
```

not:

```text
x = 1700
x = 1699
x = 1698
...
```

with every animation frame persisted to disk.

Only the final meaningful state should be persisted.

---

# 21. Interaction Controller

Mouse behavior will be isolated as much as practical.

Responsibilities:

* detect hover
* initiate expansion
* initiate drag
* calculate drag delta
* detect release
* request docking
* prevent unwanted collapse during active interaction

Conceptually:

```text
Mouse event
     ↓
InteractionController
     ↓
state transition
     ↓
NoteWindow
     ↓
NoteManager
```

---

# 22. Drag Lifecycle

Dragging should follow:

```text
Mouse Press
    ↓
Determine whether drag is allowed
    ↓
Store pointer offset
    ↓
DRAGGING
    ↓
Mouse Move
    ↓
Update window geometry
    ↓
Mouse Release
    ↓
Determine nearest edge
    ↓
Snap or retain free position
    ↓
Persist final position
```

The note should not constantly write to disk during mouse movement.

---

# 23. Hover Lifecycle

Expected flow:

```text
Mouse enters dock tab
        ↓
Check state
        ↓
If DOCKED
        ↓
EXPANDING
        ↓
Animate
        ↓
EXPANDED
```

On exit:

```text
Mouse leaves
      ↓
Check:
- editing?
- dragging?
- pointer moving toward note?
- interaction active?
      ↓
Safe to collapse?
      ↓
COLLAPSING
      ↓
DOCKED
```

The exact timing belongs to `interaction-spec.md`.

---

# 24. Persistence Timing

We should avoid saving on every tiny UI event.

Persistence should occur at meaningful boundaries.

Recommended triggers:

```text
Note created
Note deleted
Note archived
Content edit committed
Color changed
Position changed after drag
Dock state changed
Application shutdown
```

For text editing, a small debounce may be used:

```text
User typing
   ↓
wait briefly
   ↓
save
```

This prevents unnecessary disk writes.

---

# 25. Main Application Window

Comma V2 should not rely on a visible central main window.

The application's primary visual objects are the notes.

The application may still have a hidden or minimal control surface for:

* settings
* archived notes
* creating notes
* import/export
* application controls

This may eventually be accessed through:

```text
System Tray / Menu Bar
```

The exact mechanism is platform-specific and outside Phase 1.

---

# 26. Application Lifecycle

Startup:

```text
Process starts
    ↓
QApplication
    ↓
AppController
    ↓
Storage.load()
    ↓
Workspace
    ↓
NoteManager
    ↓
Create NoteWindows
    ↓
Restore geometry/state
    ↓
Desktop ready
```

Shutdown:

```text
Application shutdown
    ↓
AppController
    ↓
Collect current state
    ↓
Storage.save()
    ↓
Destroy windows
    ↓
Exit
```

---

# 27. Creation Lifecycle

Creating a note:

```text
User requests new note
        ↓
AppController / NoteManager
        ↓
Create Note model
        ↓
Persist model
        ↓
Create NoteWindow
        ↓
Register window
        ↓
Show expanded note
```

The exact default creation state will be finalized in the interaction specification.

---

# 28. Archive Lifecycle

```text
User selects Archive
        ↓
NoteWindow
        ↓
NoteManager.archive()
        ↓
Note.archived = True
        ↓
Persist
        ↓
Close NoteWindow
```

The archived note remains in storage.

---

# 29. Delete Lifecycle

Permanent deletion is different from archiving.

```text
User selects Delete
        ↓
Confirmation if required
        ↓
NoteManager
        ↓
Remove model
        ↓
Destroy window
        ↓
Persist
```

No orphaned window should remain.

---

# 30. Export Lifecycle

Export should operate on the domain model.

```text
NoteWindow
    ↓
Export requested
    ↓
NoteManager
    ↓
ExportService
    ↓
File
```

The note itself should not directly construct JSON files.

---

# 31. Proposed Project Structure

The current implementation can be gradually reorganized toward:

```text
comma/
│
├── app.py
│
├── domain/
│   ├── __init__.py
│   ├── note.py
│   └── workspace.py
│
├── application/
│   ├── __init__.py
│   ├── controller.py
│   ├── note_manager.py
│   └── dock_manager.py
│
├── presentation/
│   ├── __init__.py
│   ├── note_window.py
│   ├── note_editor.py
│   └── components/
│
├── infrastructure/
│   ├── __init__.py
│   ├── storage.py
│   ├── json_storage.py
│   └── export.py
│
├── platform/
│   ├── __init__.py
│   └── windows.py
│
├── tests/
│
├── docs/
│   ├── COMMA_V2.md
│   ├── architecture.md
│   ├── interaction-spec.md
│   ├── data-model.md
│   └── phases/
│
└── requirements.txt
```

This is the **target structure**, not a requirement to reorganize everything immediately.

---

# 32. Migration Strategy

We should avoid a dangerous "delete everything and rebuild" approach.

Instead:

```text
Current Comma
     ↓
Extract domain concepts
     ↓
Introduce new Note model
     ↓
Introduce NoteManager
     ↓
Introduce NoteWindow
     ↓
Move persistence
     ↓
Remove obsolete task UI
```

Each step should leave the project runnable.

---

# 33. Compatibility With Existing Data

The existing Comma task data should be considered during migration.

Where possible:

```text
Existing Task
     ↓
Migration
     ↓
Note
```

For example:

```text
Task.text
    → Note.content

Task.priority
    → future metadata/color/category

Task.completed
    → archive or completion metadata
```

However, no existing field should be given an artificial meaning merely to preserve compatibility.

If migration becomes ambiguous, the data migration strategy should be documented before implementation.

---

# 34. Dependency Rules

The dependency direction should be:

```text
Presentation
      ↓
Application
      ↓
Domain

Infrastructure
      ↑
Application
```

More specifically:

```text
NoteWindow
    ↓
NoteManager
    ↓
Note
```

and:

```text
NoteManager
    ↓
Storage interface
    ↓
JSONStorage
```

The domain layer should not import PyQt.

---

# 35. Error Handling

Errors should be handled at boundaries.

Examples:

### Storage failure

```text
JSON invalid
    ↓
Storage detects error
    ↓
Return safe failure / recovery
    ↓
Application continues where possible
```

### Invalid note position

```text
Saved position invalid
    ↓
DockManager validates
    ↓
Clamp/reposition
```

### Missing field

```text
Missing field
    ↓
Migration/default
    ↓
Valid Note
```

UI components should not contain JSON recovery logic.

---

# 36. Testing Architecture

Testing should exist at three levels.

### Unit

Test:

* Note model
* serialization
* migration
* dock calculations
* geometry calculations

### Integration

Test:

* NoteManager + Storage
* NoteManager + NoteWindow
* workspace restoration

### Manual UI

Test:

* hover
* expansion
* collapse
* dragging
* snapping
* multi-note interaction
* multi-monitor behavior

---

# 37. Phase Boundaries

Architecture must respect the phase roadmap.

### Phase 1 owns:

```text
Note
NoteWindow
NoteManager
Basic persistence integration
Basic editing
```

### Phase 2 owns:

```text
DockManager
Docked state
Expanded state
```

### Phase 3 owns:

```text
Animation
Hover interaction
```

### Phase 4 owns:

```text
Dragging
Snapping
Position persistence
```

### Phase 5 owns:

```text
Multi-note arrangement
Stacking
```

This prevents architecture from turning into feature creep.

---

# 38. Architectural Invariants

These rules must remain true throughout V2.

### Invariant 1

A `NoteWindow` is not the source of truth for note data.

### Invariant 2

The domain model does not depend on PyQt.

### Invariant 3

Persistence is isolated from presentation.

### Invariant 4

Global note arrangement belongs to `NoteManager` / `DockManager`, not individual notes.

### Invariant 5

Animation does not continuously mutate persistent storage.

### Invariant 6

One Comma process owns all active note windows.

### Invariant 7

A note's identity remains stable even if its window is destroyed and recreated.

### Invariant 8

Future platform-specific behavior must not leak throughout the application.

---

# 39. Request / Event Lifecycle

The general lifecycle for user actions is:

```text
                 USER
                  │
                  ▼
             NoteWindow
                  │
                  │ signal/event
                  ▼
             NoteManager
                  │
             ┌────┴────┐
             ▼         ▼
          Domain    DockManager
             │
             ▼
          Storage
             │
             ▼
          JSON
```

The UI should therefore behave as a **client of application state**, not the owner of it.

---

# 40. Final Architecture Principle

The architecture should make the following statement true:

> **A note can disappear from the screen without disappearing from the application.**

A `NoteWindow` is temporary.

A `Note` is persistent.

This distinction is the heart of Comma V2.

```text
NoteWindow
   = representation

Note
   = identity + state

NoteManager
   = coordination

Storage
   = persistence

AppController
   = lifecycle
```

If these boundaries remain clean, the rest of Comma V2 can evolve without requiring another architectural rewrite.
