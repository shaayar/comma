# Comma V2

## Data Model Specification

**Status:** Draft
**Version:** 2.0
**Parent:** `COMMA_V2.md`
**Related:** `architecture.md`, `interaction-spec.md`

---

# 1. Purpose

This document defines the data structures used by Comma V2 and the state that must persist between application sessions.

The primary principle is:

> **The note model represents what exists. The UI represents what is currently being shown.**

A note must remain valid even if its associated window is destroyed.

---

# 2. Core Entities

Comma V2 initially contains four persistent concepts:

```text
Workspace
│
├── Settings
│
└── Notes
     ├── Note
     ├── Note
     └── Note
```

There are also temporary runtime concepts:

```text
Runtime
├── NoteWindow
├── UI state
└── Animation state
```

Runtime objects are **not automatically persisted**.

---

# 3. Workspace

`Workspace` represents the complete persisted Comma environment.

Conceptual model:

```python
@dataclass
class Workspace:
    schema_version: int
    notes: list[Note]
    settings: Settings
```

Example:

```json
{
  "schema_version": 2,
  "notes": [],
  "settings": {}
}
```

---

# 4. Schema Version

Every persisted workspace must contain:

```json
"schema_version": 2
```

This allows future versions to migrate older data.

The application must never assume that an arbitrary JSON file represents the current schema.

Loading flow:

```text
JSON
 ↓
Read schema_version
 ↓
Migration if necessary
 ↓
Validate
 ↓
Workspace
```

---

# 5. Note Identity

Every note requires a stable unique identifier.

Example:

```json
"id": "01JXXXXXXXXXXXX"
```

The exact ID-generation mechanism is an implementation decision.

Requirements:

* unique
* stable
* never regenerated simply because a window is recreated
* persisted
* safe to use as a dictionary key

The ID belongs to the note, not its window.

---

# 6. Note

The initial V2 note model is:

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
    docked: bool
    order: int

    archived: bool
```

This is the initial contract.

Fields should not be added simply because they might be useful later.

---

# 7. Note Fields

## 7.1 `id`

Unique persistent identifier.

Example:

```text
"note-001"
```

Purpose:

* identify a note
* associate model with window
* persistence
* future references

---

## 7.2 `title`

Short human-readable note title.

Example:

```text
"Groceries"
```

The title is optional from a product perspective, but the model should support it from V2 onward.

If omitted during migration:

```text
title = "Untitled"
```

---

## 7.3 `content`

The actual note body.

Example:

```text
Apple
Pineapple
Ginger
```

Content is stored as text.

V2 does not require rich-text storage.

---

# 8. Text Model

The initial content representation is:

```text
plain text
```

This intentionally avoids introducing:

* HTML
* Markdown rendering
* rich text metadata
* embedded media
* document trees

The editor may later support richer content, but the persistence model should not prematurely assume it.

---

# 9. Color

Each note has a persistent visual color.

Example:

```json
"color": "#F5D76E"
```

The exact palette is defined by the UI/theme layer.

The data model stores the selected color identity.

Color should not be used to encode critical semantic information.

---

# 10. Position

A note has desktop coordinates:

```json
"position": {
  "x": 1500,
  "y": 240
}
```

Conceptually represented internally as:

```python
x: int
y: int
```

The coordinate system follows Qt's desktop/screen coordinate system.

---

# 11. Dimensions

The initial model stores:

```text
width
height
```

This allows future support for:

* user resizing
* restoring custom dimensions
* different note sizes

V2 may initially use fixed dimensions while still persisting the fields.

This avoids a schema migration later when resizing is introduced.

---

# 12. Dock Edge

The note stores the edge to which it is associated.

Initial value:

```text
"right"
```

Supported architectural values:

```text
"left"
"right"
"top"
"bottom"
```

Only `"right"` is required for the first implementation.

---

# 13. Docked State

The note stores:

```json
"docked": true
```

Meaning:

```text
true
→ note currently belongs to the docked interaction state

false
→ note currently exists in free/expanded desktop space
```

This is persistent state.

The runtime animation state is not persisted.

---

# 14. Order

Docked notes require deterministic ordering.

Initial representation:

```json
"order": 0
```

Example:

```text
Note A → order 0
Note B → order 1
Note C → order 2
```

The implementation may eventually replace explicit integer ordering with a workspace list order.

The persistent contract only requires that ordering be deterministic.

---

# 15. Archive State

The model contains:

```json
"archived": false
```

When:

```text
false
```

the note is active.

When:

```text
true
```

the note is archived and should not appear on the active desktop.

Archiving is non-destructive.

---

# 16. Archived Notes

Archived notes remain part of the workspace.

Example:

```text
Workspace
│
├── Active notes
│
└── Archived notes
```

We do not need a separate archive database in V2.

The same `Note` model can represent both.

---

# 17. Runtime State vs Persistent State

This distinction is critical.

### Persistent

```text
id
title
content
color
position
dimensions
edge
docked
order
archived
```

### Runtime only

```text
hovered
focused
dragging
animating
mouse position
animation progress
current interaction
```

Runtime state must not be written into JSON.

---

# 18. Why Animation State Is Not Persisted

Suppose Comma closes while a note is expanding.

We should not save:

```text
"animation_progress": 0.63
```

Instead, the application resolves the note to a stable state.

For example:

```text
EXPANDING
   ↓
application shutdown
   ↓
resolve to DOCKED or EXPANDED
   ↓
save
```

The exact shutdown policy belongs to the controller.

---

# 19. Settings

Workspace-level settings are separate from note-level data.

Initial conceptual model:

```python
@dataclass
class Settings:
    theme: str
    default_edge: str
```

Potential future settings:

```text
animation_speed
collapse_delay
startup_behavior
keyboard_shortcuts
```

These should only be added when implemented.

---

# 20. Example Complete Workspace

A representative persisted workspace:

```json
{
  "schema_version": 2,

  "settings": {
    "theme": "dark",
    "default_edge": "right"
  },

  "notes": [
    {
      "id": "note-001",
      "title": "Groceries",
      "content": "Apple\nPineapple\nGinger",
      "color": "#F5D76E",

      "x": 1560,
      "y": 180,
      "width": 320,
      "height": 420,

      "edge": "right",
      "docked": true,
      "order": 0,
      "archived": false
    }
  ]
}
```

This is illustrative.

The exact JSON schema should be finalized alongside implementation.

---

# 21. Validation

Loaded data must be validated before becoming runtime state.

Validation should check:

### Required

```text
schema_version
notes
```

### Note

```text
id
title
content
color
position
edge
docked
order
archived
```

### Types

Examples:

```text
id        → string
title     → string
content   → string
x         → integer
y         → integer
width     → integer
height    → integer
docked    → boolean
archived  → boolean
```

Invalid data should be rejected or repaired safely.

---

# 22. Defensive Defaults

When possible, missing non-critical fields should receive defaults.

Example:

```text
missing title
→ "Untitled"

missing color
→ default note color

missing edge
→ configured default edge

missing width/height
→ default dimensions
```

Critical identity corruption should not be silently ignored.

---

# 23. Position Validation

Persisted coordinates cannot be assumed to remain valid forever.

Reasons include:

* monitor removed
* monitor layout changed
* resolution changed
* display scaling changed
* laptop disconnected from external monitor

Therefore:

```text
Stored position
      ↓
Validate against current screens
      ↓
Valid?
 ┌────┴────┐
Yes       No
 │         │
 ↓         ↓
Restore   Reposition
```

The `DockManager` is responsible for final geometry correction.

---

# 24. Multi-Monitor Data

The initial model does **not** persist a monitor hardware identifier.

We intentionally avoid storing:

```text
monitor_serial
monitor_id
display_name
```

because these identifiers are platform-dependent and unreliable across configurations.

The note stores desktop coordinates and dock edge.

Future multi-monitor logic can improve restoration without changing the basic note identity.

---

# 25. Migration From Current Comma

The existing Comma model contains task-oriented concepts such as:

```text
text
priority
completed
category
```

V2 is note-oriented.

Migration should therefore be conservative.

Potential mapping:

```text
Task.text
    ↓
Note.content
```

Potential title:

```text
Task category
    ↓
Note.title
```

or:

```text
"Untitled"
```

if no meaningful title exists.

---

# 26. Priority Migration

Existing priority should **not automatically become note color** unless explicitly decided.

Although:

```text
High → red
Medium → yellow
Low → green
```

is tempting, it changes the meaning of color.

Instead, priority should either:

1. remain as future metadata, or
2. be migrated only if V2 explicitly preserves task semantics.

This decision belongs to the migration plan.

---

# 27. Completion Migration

Existing completed tasks should not automatically become archived notes without an explicit migration rule.

Completion and archival represent different concepts:

```text
Completed
≠
Archived
```

If migration needs to preserve completed tasks, that requirement must be separately defined.

---

# 28. Data Ownership

The ownership hierarchy is:

```text
Workspace
   │
   ├── Settings
   │
   └── Notes
        │
        ├── Note A
        ├── Note B
        └── Note C
```

`NoteManager` owns the runtime collection.

`Storage` owns serialization.

`NoteWindow` does not own the persistent note.

---

# 29. Runtime Mapping

At runtime:

```text
NoteManager
│
├── note-001 → Note
│              └→ NoteWindow
│
├── note-002 → Note
│              └→ NoteWindow
│
└── note-003 → Note
               └→ NoteWindow
```

A window can be destroyed without destroying the model.

A new window can later be created for the same model.

---

# 30. Serialization Boundary

Serialization should happen only at the infrastructure boundary.

Preferred:

```text
Note
 ↓
Serializer
 ↓
dict
 ↓
JSON
```

Not:

```text
NoteWindow
 ↓
JSON
```

This keeps the data format independent from PyQt widgets.

---

# 31. Version Migration

Future schema changes should follow:

```text
schema 2
   ↓
migration
   ↓
schema 3
```

Migration functions should be explicit.

Conceptually:

```python
migrate_v1_to_v2(data)
migrate_v2_to_v3(data)
```

Avoid a single giant function containing every historical version.

---

# 32. Unknown Fields

The loader should tolerate unknown fields where practical.

Example:

```json
{
  "id": "note-001",
  "content": "Hello",
  "future_feature": true
}
```

Older Comma versions should not crash merely because additional fields exist.

Unknown fields do not need to be preserved unless forward compatibility requires it.

---

# 33. Delete Semantics

Permanent deletion removes the note from the workspace.

After deletion:

```text
Note model
    ↓
removed
    ↓
window destroyed
    ↓
persisted workspace updated
```

The ID should not be reused immediately.

---

# 34. Archive Semantics

Archive changes:

```text
archived = false
```

to:

```text
archived = true
```

The following remain unchanged:

```text
id
content
title
color
position
```

This allows reliable restoration.

---

# 35. Note Creation Defaults

A newly created note receives:

```text
unique ID
default title
empty content
default color
default dimensions
default dock edge
default ordering
archived = false
```

The new note should normally be shown immediately in an interactive state.

The exact visual creation behavior is defined in the interaction specification.

---

# 36. Default Values

Initial conceptual defaults:

```text
title      = "Untitled"
content    = ""
color      = default palette color
edge       = "right"
docked     = false during initial creation
archived   = false
order      = next available order
dimensions = default note size
```

These values are implementation defaults, not immutable product requirements.

---

# 37. Fields Explicitly Deferred

The following are intentionally **not part of the initial persistent model**:

```text
tags
attachments
images
rich text
markdown
reminders
due dates
notifications
cloud IDs
sync metadata
user accounts
sharing permissions
AI metadata
```

They may be introduced later through schema versions.

---

# 38. Data Integrity Rules

The following must always be true:

### Rule 1

Every active note has a unique ID.

### Rule 2

Every note has valid content.

Empty content is valid.

### Rule 3

Archived notes remain persisted.

### Rule 4

A window does not determine whether a note exists.

### Rule 5

Deleting a window does not necessarily delete the note.

### Rule 6

Deleting a note must destroy/remove its associated runtime window.

### Rule 7

Persistent data contains stable state, not transient animation state.

### Rule 8

Schema version is always explicit.

---

# 39. Data Model Definition of Done

The data model is considered complete for V2 when:

* Notes have stable IDs.
* Notes have independent persistent content.
* Notes have persistent appearance.
* Notes have persistent geometry.
* Notes have persistent dock state.
* Notes have deterministic ordering.
* Archived notes remain recoverable.
* Workspace schema is versioned.
* Invalid persisted data can be handled safely.
* Existing Comma data has a documented migration strategy.
* Runtime UI state is clearly separated from persistent state.
* Future schema changes have a defined migration mechanism.

---

# 40. Final Data Principle

Comma V2 must preserve this distinction:

```text
                 PERSISTENT
                     │
                     ▼
              ┌─────────────┐
              │    Note     │
              │             │
              │ identity    │
              │ content     │
              │ appearance  │
              │ geometry    │
              │ lifecycle   │
              └──────┬──────┘
                     │
                     ▼
                 RUNTIME
                     │
                     ▼
              ┌─────────────┐
              │ NoteWindow  │
              │             │
              │ hover       │
              │ focus       │
              │ animation   │
              │ dragging    │
              └─────────────┘
```

> **The note is the thing. The window is merely how the thing appears.**
