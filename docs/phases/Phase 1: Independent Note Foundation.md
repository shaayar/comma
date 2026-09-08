# Phase 1: Independent Note Foundation

**Project:** Comma V2
**Phase:** 1
**Status:** Planned
**Primary Goal:** Establish Comma as a collection of independent desktop note windows rather than a single task-list application.

---

## 1. Phase Objective

Replace the current single-window task-list foundation with the first real building block of Comma V2:

> **A Note is an independent piece of data, and a NoteWindow is its visual representation on the desktop.**

Phase 1 establishes the separation between:

```text
Note Model
    ↓
NoteManager
    ↓
NoteWindow
```

The user should be able to create multiple notes and interact with each note independently.

This phase is about creating the **foundation**, not reproducing the complete reference behavior.

---

## 2. What We Are Building

At the end of Phase 1, Comma should behave conceptually like:

```text
                 ┌─────────────────┐
                 │   AppController │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │   NoteManager   │
                 └───────┬─────────┘
                         │
             ┌───────────┼───────────┐
             │           │           │
        ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
        │  Note   │ │  Note   │ │  Note   │
        │ Window  │ │ Window  │ │ Window  │
        └─────────┘ └─────────┘ └─────────┘
```

Each note must have its own window.

Creating three notes should result in three independent note windows rather than three entries inside a central list.

---

# 3. Scope

## 3.1 Note Model

Create a dedicated `Note` domain model.

For Phase 1, the model must support at minimum:

```text
id
title
content
color
```

The model should be independent of PyQt.

It must not contain:

* QWidget references
* signals
* event handlers
* UI state
* persistence logic
* animation logic

The model represents **what the note is**, not how it appears.

---

## 3.2 NoteManager

Create a `NoteManager` responsible for managing active notes.

Responsibilities:

* create notes
* store active notes
* retrieve notes by ID
* remove notes
* create/destroy associated windows
* maintain the relationship between a `Note` and its `NoteWindow`

Conceptually:

```python
note = Note(...)
manager.add(note)

window = manager.create_window(note.id)
```

The manager becomes the owner of application-level note state.

---

## 3.3 Independent NoteWindow

Create a dedicated `NoteWindow`.

Each note should appear as its own desktop window.

The window should:

* display the note title
* display/edit the note content
* display the note color
* allow direct text editing
* visually behave as an independent note
* be capable of existing alongside other note windows

The window should receive a `Note` from the manager rather than becoming the source of truth.

---

## 3.4 Basic Note Creation

There must be a simple way to create a new note.

The creation flow should be:

```text
User creates note
        ↓
NoteManager creates Note
        ↓
NoteManager creates NoteWindow
        ↓
Window becomes visible
        ↓
User can immediately type
```

A newly created note should be focused and ready for editing.

The exact final creation UI is intentionally not locked in during this phase.

It may temporarily be a simple development button/menu/shortcut if necessary.

---

## 3.5 Multiple Notes

The application must support multiple simultaneous notes.

Example:

```text
┌───────────────┐
│ Shopping      │
│               │
│ Milk          │
│ Bread         │
│ Eggs          │
└───────────────┘


                    ┌───────────────┐
                    │ Ideas         │
                    │               │
                    │ New project   │
                    └───────────────┘


        ┌───────────────┐
        │ TODO          │
        │               │
        │ Fix login     │
        └───────────────┘
```

Each window must be independently editable.

Changing one note must not accidentally modify another note.

---

# 4. Window Behavior

Phase 1 establishes the existence of independent note windows.

The windows should have a lightweight desktop-note appearance rather than resembling the existing task manager.

The following are allowed:

* frameless windows
* custom title/header
* compact dimensions
* always-on-top behavior
* simple note-like styling
* basic window controls if needed during development

However, these should remain implementation details.

The visual design is **not** the primary objective of Phase 1.

---

# 5. Data Flow

The required data flow is:

```text
User Input
    ↓
NoteWindow
    ↓
Note / NoteManager
```

The window may update the model when the user edits the note.

The important rule is:

> `NoteWindow` must never become the application's permanent source of truth.

For example, this architecture is acceptable:

```python
note.content = editor.toPlainText()
```

This architecture is not:

```python
window.editor_contents = ...
# application treats the widget itself as the note
```

The model must remain independently accessible.

---

# 6. Basic Editing

Phase 1 supports:

### Title

The user can set or edit the note title.

### Content

The user can type normal plain text.

### Color

A note may have a basic color.

The exact color-selection UI is not important yet.

Rich text, Markdown, formatting controls, attachments, images, and other content systems are explicitly excluded.

---

# 7. Application Structure

The target structure should begin moving toward:

```text
comma/
├── app.py
│
├── domain/
│   └── note.py
│
├── application/
│   ├── controller.py
│   └── note_manager.py
│
├── presentation/
│   └── note_window.py
│
├── infrastructure/
│   └── storage.py
│
├── tests/
│   ├── test_note.py
│   └── test_note_manager.py
│
└── docs/
    └── phases/
        └── phase-01-note-windows.md
```

This is a directional structure.

Phase 1 does **not** require a massive repository rewrite if the same architectural separation can be achieved incrementally.

---

# 8. AppController

Introduce an application-level controller.

Responsibilities:

* initialize `QApplication`
* initialize `NoteManager`
* manage application lifecycle
* create the initial workspace
* keep the application alive while note windows exist
* coordinate shutdown

The controller should not contain note-rendering logic.

---

# 9. Legacy Task Manager

The current task-management UI is no longer the target architecture.

The old concepts:

```text
Task
TaskWidget
ToDoApp
priority
completed
task list
```

should not be carried forward into the new note architecture merely because they already exist.

During implementation:

* reuse useful infrastructure where appropriate
* extract reusable concepts where useful
* do not preserve task-specific architecture for compatibility's sake
* do not build the new system around `ToDoApp`

The nested React application is also not part of the V2 implementation path.

---

# 10. Persistence Boundary

Full workspace persistence belongs to a later phase.

Phase 1 should nevertheless establish the **storage boundary** so that UI code does not become responsible for persistence.

The architecture should allow:

```text
NoteManager
     ↓
Storage
```

without:

```text
NoteWindow
     ↓
tasks.json
```

Full persistence of:

* position
* size
* dock state
* order
* archived state
* workspace configuration

is explicitly deferred.

A temporary in-memory implementation is acceptable during Phase 1.

---

# 11. Explicitly Out of Scope

The following must **not** be implemented as part of Phase 1.

## Docking

No edge docking.

```text
Desktop edge
████████████
```

No right-edge tab behavior.

---

## Hover Reveal

No:

```text
hover → note slides in
```

No hover-triggered expansion.

---

## Animation

No reveal/collapse animations.

No animated docking.

No animation state machine implementation.

---

## Dragging

No drag-to-rearrange behavior.

No edge snapping.

No drag thresholds.

---

## Multiple-Note Arrangement

Multiple notes may exist, but Phase 1 does not define how they should be automatically arranged.

Do not build the final vertical dock stack.

---

## Archive

No archive workflow.

---

## Export

No export workflow.

---

## Final Visual Design

Do not spend Phase 1 turning the application into a pixel-perfect recreation of the reference.

Visual polish belongs later.

---

## Advanced Editing

Do not implement:

* Markdown
* rich text
* formatting toolbar
* attachments
* images
* links
* checklists
* tags
* reminders
* due dates

---

# 12. Window Lifecycle

A critical architectural distinction must be established:

```text
Note lifecycle
      ≠
Window lifecycle
```

A `Note` is application data.

A `NoteWindow` is its current visual representation.

Therefore:

```text
Note created
    ↓
Window created
```

but:

```text
Window destroyed
    ≠
Note automatically deleted
```

The manager must own the relationship.

This distinction is important because future phases will need to hide, dock, collapse, expand, destroy, and recreate windows without destroying the underlying note.

---

# 13. Testing Requirements

Phase 1 should introduce basic automated tests.

## Note tests

Verify:

* a note can be created
* every note receives a unique ID
* title is stored correctly
* content is stored correctly
* color is stored correctly
* empty content is valid

---

## NoteManager tests

Verify:

* notes can be added
* notes can be retrieved by ID
* notes can be removed
* multiple notes can coexist
* one note can be modified without affecting another

---

## Window integration tests

At minimum, manually verify:

### Test 1: Create

Create a note.

Expected:

```text
A standalone note window appears.
```

### Test 2: Create multiple

Create three notes.

Expected:

```text
Three independent windows exist.
```

### Test 3: Edit

Edit Note A.

Expected:

```text
Note A changes.
Note B and Note C remain unchanged.
```

### Test 4: Focus

Click between multiple notes.

Expected:

```text
Each note can receive focus independently.
```

### Test 5: Model separation

Change a note through the UI.

Expected:

```text
The corresponding Note model contains the updated data.
```

### Test 6: No task-list regression

The new application should not open the old central task-list interface as its primary UI.

---

# 14. Acceptance Criteria

Phase 1 is complete only when all of the following are true:

* [ ] Comma starts through the new application controller.
* [ ] A dedicated `Note` model exists.
* [ ] `Note` has no PyQt dependency.
* [ ] A dedicated `NoteManager` exists.
* [ ] A dedicated `NoteWindow` exists.
* [ ] Notes are represented independently from their windows.
* [ ] A user can create a note.
* [ ] A newly created note opens as an independent desktop window.
* [ ] Multiple note windows can exist simultaneously.
* [ ] Each note can be edited independently.
* [ ] Title and content are represented in the note model.
* [ ] Basic color is represented in the note model.
* [ ] Window code does not directly own persistence.
* [ ] No docking behavior exists yet.
* [ ] No hover-reveal behavior exists yet.
* [ ] No drag/snap behavior exists yet.
* [ ] No archive/export system exists yet.
* [ ] Basic domain/manager tests pass.
* [ ] The old task-list window is no longer the V2 application foundation.

---

# 15. Phase 1 Definition of Done

Phase 1 is not judged by how closely the application resembles the final reference.

It is judged by whether Comma has successfully crossed this architectural boundary:

### Before

```text
Single Application Window
        ↓
Task List
        ↓
Task Widgets
```

### After

```text
Application Controller
        ↓
    NoteManager
        ↓
 ┌──────┼──────┐
 ↓      ↓      ↓
Note   Note   Note
 ↓      ↓      ↓
Window Window Window
```

Once this boundary is stable, later phases can add docking, hover reveal, animation, dragging, arrangement, persistence, and polish without rebuilding the foundation.

---

# 16. Phase Gate

Do not begin Phase 2 until Phase 1 passes its acceptance criteria.

The next phase should only begin after we confirm:

> **Independent notes work reliably, and the model, manager, and window responsibilities are cleanly separated.**

Phase 2 will then introduce the **desktop-edge docking system**.

No Phase 2 behavior should be quietly added to Phase 1 simply because it is convenient during implementation.
