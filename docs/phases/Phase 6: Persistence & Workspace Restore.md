# Phase 6: Persistence & Workspace Restoration

**Project:** Comma V2
**Phase:** 6
**Status:** Planned
**Primary Goal:** Persist the complete Comma workspace and reliably restore it after application restart.

---

# 1. Phase Objective

Until now, Comma's notes primarily exist during the current application session.

Phase 6 gives Comma memory.

When the user:

* creates a note
* edits its content
* changes its title
* changes its color
* moves it
* docks it
* rearranges it
* changes its size

Comma must eventually be able to restore that state.

The intended lifecycle becomes:

```text
Session 1
─────────

Create notes
     ↓
Edit
     ↓
Move
     ↓
Dock
     ↓
Rearrange
     ↓
Quit


Session 2
─────────

Launch Comma
     ↓
Load workspace
     ↓
Recreate notes
     ↓
Restore state
     ↓
Desktop looks as it was left
```

The key principle is:

> **Restarting Comma should not feel like starting Comma from scratch.**

---

# 2. What We Are Building

Phase 6 introduces complete persistence for the current V2 workspace model.

This includes:

* note identity
* title
* content
* color
* position
* dimensions
* dock state
* dock edge
* dock order
* archived state
* workspace settings
* schema version
* loading
* saving
* validation
* migration foundation
* recovery from malformed data

---

# 3. Persistence Architecture

The architecture becomes:

```text id="f5j2k8"
                  AppController
                       │
                load workspace
                       │
                       ▼
                    Storage
                       │
                       ▼
                  NoteManager
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Note Models         Note Windows
             │                   │
             └─────────┬─────────┘
                       │
                  state changes
                       │
                       ▼
                    Storage
```

The important separation remains:

```text
NoteWindow
    ≠
Storage
```

A window must never directly decide how JSON is structured.

---

# 4. Storage Interface

The infrastructure layer should expose a storage abstraction.

Conceptually:

```python
class Storage:
    def load_workspace(self):
        ...

    def save_workspace(self, workspace):
        ...
```

The exact implementation can differ.

The important requirement is that the rest of Comma should not care whether the data is stored in:

```text
JSON
SQLite
another local format
```

The current implementation should use JSON.

---

# 5. JSON Storage

Implement:

```text id="m8q4s1"
infrastructure/json_storage.py
```

The JSON file becomes the persistent representation of the workspace.

The application should have one authoritative workspace file.

Do not create one JSON file per note unless there is a strong implementation reason.

---

# 6. Workspace Schema

The persisted structure should follow the model established earlier.

Conceptually:

```json
{
  "schema_version": 1,
  "settings": {
    "theme": "default",
    "default_edge": "right"
  },
  "notes": [
    {
      "id": "unique-id",
      "title": "My Note",
      "content": "Remember this",
      "color": "yellow",
      "x": 1200,
      "y": 200,
      "width": 300,
      "height": 250,
      "edge": "right",
      "docked": true,
      "order": 0,
      "archived": false
    }
  ]
}
```

This is the conceptual schema.

The exact color representation and settings values may evolve.

---

# 7. Schema Version

The workspace must include:

```text id="q6m1x8"
schema_version
```

This is mandatory.

Example:

```json
{
  "schema_version": 1
}
```

The purpose is to allow future Comma versions to understand older workspace files.

Do not assume today's JSON structure will remain unchanged forever.

---

# 8. Note Identity

The `id` of a note must remain stable.

Example:

```text id="t9r3v2"
Note ID:
550e8400-e29b-41d4-a716-446655440000
```

The actual ID generation mechanism may differ.

The requirement is:

> Loading a workspace must restore the same logical note identity.

The ID must not be regenerated every time the application launches.

---

# 9. Persisted Note Fields

The complete V2 note record should support:

```text id="p3n7w5"
id
title
content
color
x
y
width
height
edge
docked
order
archived
```

Each field has a specific purpose.

### `id`

Stable note identity.

### `title`

User-visible note title.

### `content`

Plain-text note content.

### `color`

Visual note color.

### `x`, `y`

Floating/docked desktop position.

### `width`, `height`

Note dimensions.

### `edge`

Current dock edge.

Initial valid value:

```text
right
```

### `docked`

Whether the note currently belongs to the dock.

### `order`

Vertical ordering among docked notes.

### `archived`

Whether the note is archived.

Archive behavior itself belongs to Phase 7.

---

# 10. Workspace Settings

Workspace-level settings should also have a dedicated section.

Initially:

```text id="f4w7n2"
settings
├── theme
└── default_edge
```

Do not store transient UI information here.

For example, do not persist:

```text
hovered
focused
dragging
animating
mouse_position
collapse_timer
```

Those are runtime state.

---

# 11. Runtime State vs Persistent State

This distinction must remain strict.

## Persistent

```text id="g3x8k2"
Note identity
Content
Title
Color
Position
Size
Dock state
Dock order
Archive state
```

## Runtime

```text id="m5q9r1"
Hovered
Focused
Dragging
Animating
Animation progress
Mouse position
Collapse timer
Active interaction
```

Runtime state disappears when Comma exits.

Persistent state survives.

---

# 12. Application Startup

Startup flow:

```text id="v8k2s5"
Application starts
       ↓
Initialize Storage
       ↓
Load workspace
       ↓
Validate workspace
       ↓
Create Note models
       ↓
Register with NoteManager
       ↓
Create NoteWindows
       ↓
Restore geometry/state
       ↓
Arrange dock
       ↓
Show workspace
```

The UI should not independently reconstruct itself from the JSON file.

The workspace should first become domain/application state.

---

# 13. Application Shutdown

Shutdown flow:

```text id="q7m4x9"
Application shutdown requested
          ↓
Collect current workspace
          ↓
Serialize stable state
          ↓
Write storage
          ↓
Destroy application
```

The save operation must happen before the application fully exits.

---

# 14. Autosave

Comma should not rely exclusively on application shutdown.

State changes should be saved during normal usage.

However:

> **Do not write to disk on every keystroke.**

For example, this would be inefficient:

```text id="d8p1y4"
H → save
e → save
l → save
l → save
o → save
```

Instead, text changes should use debounced saving.

Conceptually:

```text id="j3r8m6"
User types
   ↓
mark workspace dirty
   ↓
wait briefly
   ↓
save
```

The exact debounce interval is configurable.

---

# 15. Save Triggers

A workspace save should occur after meaningful state changes such as:

* note content changes
* title changes
* color changes
* note creation
* note removal
* position changes
* docking
* undocking
* reordering
* size changes
* archive state changes

The system should avoid excessive writes during continuous operations.

---

# 16. Drag Persistence

Dragging creates a special case.

Do not save the workspace for every mouse-move event.

Bad:

```text id="x2f8s6"
mouse move
→ save
mouse move
→ save
mouse move
→ save
...
```

Correct:

```text id="z6q3m1"
drag begins
     ↓
position changes in memory
     ↓
drag ends
     ↓
mark workspace dirty
     ↓
save
```

This keeps interaction responsive.

---

# 17. Dock Rearrangement Persistence

When a docked note changes order:

```text id="p5v9k2"
A
B
C

drag C above A

C
A
B
```

the resulting order must be persisted.

After restart:

```text id="s8x3n7"
C
A
B
```

must be restored.

---

# 18. Window Geometry Persistence

For floating notes, persist:

```text id="u7m2q4"
x
y
width
height
```

This allows:

```text id="n4x8c1"
floating note
     ↓
quit
     ↓
restart
     ↓
same position and size
```

For docked notes, dock layout should remain authoritative.

The saved `x` coordinate should not override the dock calculation if the note is docked.

---

# 19. Dock State Restoration

If a note was docked before shutdown:

```text id="b5k7m2"
docked = true
edge = "right"
```

on restart:

```text id="r8q1v6"
load
 ↓
NoteManager
 ↓
DockManager
 ↓
restore dock
```

The note should return to the dock.

The dock should calculate its final geometry rather than blindly trusting an old screen coordinate.

---

# 20. Dock Order Restoration

Docked notes should restore according to their saved `order`.

Example:

```text id="x9p3k6"
Saved:
A → 2
B → 0
C → 1
```

Restored:

```text id="c7m1v4"
B
C
A
```

After loading, the order should be normalized if necessary.

---

# 21. Invalid Order Recovery

If malformed or legacy data contains:

```text id="q3w8n2"
A → 0
B → 0
C → 17
```

Comma must not crash.

The loader should normalize the order deterministically.

A reasonable strategy:

1. preserve valid relative ordering where possible
2. resolve duplicates
3. assign sequential order values
4. re-layout the dock

Result:

```text id="z4r7p1"
A → 0
B → 1
C → 2
```

---

# 22. Invalid Geometry Recovery

Stored geometry may become invalid.

Examples:

* negative dimensions
* enormous dimensions
* position outside all available screens
* old monitor configuration
* corrupted coordinates

Comma should validate geometry before creating the final window.

If invalid:

```text id="v2n5x8"
stored geometry
     ↓
validation fails
     ↓
safe default geometry
```

The note itself must not be lost merely because its old position is invalid.

---

# 23. Multi-Monitor Consideration

Phase 6 should support reasonable recovery when the user changes monitor configuration.

Do not persist fragile monitor hardware identifiers as the primary source of truth.

For example:

```text id="g8s2m5"
Laptop + external monitor
       ↓
external monitor removed
       ↓
restart
       ↓
note would otherwise be off-screen
```

Comma should detect the invalid position and move the note to a visible safe location.

The note's content and identity must remain intact.

---

# 24. Atomic Saving

Workspace saving should avoid leaving a half-written file if the application crashes during a write.

The preferred strategy is conceptually:

```text id="j7x3m9"
workspace.json
      ↓
write temporary file
      ↓
flush/close
      ↓
replace original
```

The exact implementation can vary by platform.

The principle is:

> A failed save should not casually destroy the previous valid workspace.

---

# 25. Corrupted Workspace

If the workspace file cannot be parsed:

```text id="k2v6s4"
Load
 ↓
JSON invalid
```

Comma should:

1. avoid crashing
2. preserve the corrupted file for recovery if possible
3. start with a safe empty/default workspace
4. make the failure diagnosable

Do not silently overwrite a potentially recoverable workspace with a blank file.

---

# 26. Missing Workspace

If no workspace file exists:

```text id="m9r3w7"
No file
 ↓
create default workspace
 ↓
start Comma normally
```

The first save creates the workspace file.

---

# 27. Partial Data

If a note is missing optional fields:

```text id="p1x8q4"
{
    "id": "...",
    "content": "Hello"
}
```

the loader should apply safe defaults for missing fields.

For example:

```text id="c5v2n7"
title    → "Untitled"
color    → default color
width    → default width
height   → default height
edge     → "right"
docked   → false
order    → next valid order
archived → false
```

Required identity/data should still be validated.

---

# 28. Data Validation

The storage layer should validate loaded data before handing it to the application.

Validation should check:

* schema version
* workspace structure
* note structure
* note ID validity
* duplicate IDs
* field types
* geometry values
* valid edge values
* valid order values
* archive value
* settings structure

Invalid fields should be repaired where safely possible.

Invalid notes should only be discarded when they cannot be safely reconstructed.

---

# 29. Duplicate Note IDs

If corrupted data contains:

```text id="w5n8c2"
Note A → ID X
Note B → ID X
```

Comma must not allow ambiguous identity.

The loader should resolve the conflict deterministically.

The exact recovery strategy can be finalized during implementation.

The important invariant is:

> Every active note must have one unique stable ID.

---

# 30. Migration Foundation

Phase 6 establishes the migration mechanism.

Conceptually:

```text id="t6r2p9"
load JSON
   ↓
read schema_version
   ↓
if old:
    migrate
   ↓
validate
   ↓
load current model
```

Future schema changes should not require rewriting the entire application loader.

---

# 31. Old Comma Data

The previous application uses a task-oriented structure.

Migration should be conservative.

Potential mapping:

```text id="h3x7m1"
Task.text
   ↓
Note.content
```

Potential title:

```text id="n8q2v5"
Task category / fallback
   ↓
Note.title
```

However:

```text id="r4k9s3"
Task.priority
   ≠
Note.color
```

and:

```text id="y6p1w8"
Task.completed
   ≠
Note.archived
```

unless explicitly decided later.

Semantic meaning must not be invented during migration.

---

# 32. Save Debouncing

The persistence system should provide a dirty-state concept.

Conceptually:

```text id="v3k8q5"
workspace_dirty = true
```

Then:

```text id="f7m2x9"
state change
   ↓
mark dirty
   ↓
debounce
   ↓
save
   ↓
mark clean
```

The exact mechanism can use Qt timers or another appropriate application-level approach.

---

# 33. Persistence Ownership

Persistence responsibility should follow:

```text id="s9x4k1"
Note
  ↓
NoteManager / Workspace
  ↓
Storage
  ↓
JSON
```

Not:

```text id="d5p8m2"
NoteWindow
  ↓
open("workspace.json")
```

The UI should never know the storage file format.

---

# 34. What Phase 6 Does NOT Do

## Archive UI

Not yet.

The `archived` field may now persist because the data model supports it, but the user-facing archive workflow belongs to Phase 7.

---

## Export

Not yet.

Workspace persistence is different from user-requested note export.

---

## Cloud Sync

Not included.

No:

* accounts
* authentication
* cloud database
* synchronization
* conflict resolution

---

## Multiple Devices

Not included.

---

## Backup Management UI

Not included.

Atomic saves and corruption recovery are sufficient for this phase.

---

## Rich Content Persistence

Only plain text is persisted.

No:

* HTML
* Markdown rendering state
* attachments
* images
* embedded files

---

# 35. Testing

## Test 1: Basic Restart

1. Create a note.
2. Add title and content.
3. Quit Comma.
4. Restart.

Expected:

* same note exists
* title is restored
* content is restored

---

## Test 2: Multiple Notes

Create:

```text id="k3x8m1"
A
B
C
```

Restart.

Expected:

```text id="r7q2v5"
A
B
C
```

All notes remain independent.

---

## Test 3: Floating Geometry

1. Move a note.
2. Resize it.
3. Quit.
4. Restart.

Expected:

* position restored
* dimensions restored

---

## Test 4: Dock State

1. Dock a note.
2. Quit.
3. Restart.

Expected:

```text id="x5m9q2"
docked = true
```

and the note returns to the right-edge dock.

---

## Test 5: Dock Order

Start:

```text id="w2v6n8"
A
B
C
```

Rearrange:

```text id="p4x9r1"
C
A
B
```

Restart.

Expected:

```text id="m7q3k5"
C
A
B
```

---

## Test 6: Content During Rapid Typing

Type quickly.

Expected:

* no lost characters
* no UI freezes
* eventual save succeeds

---

## Test 7: Position During Drag

Move a note continuously.

Expected:

* no save operation occurs on every mouse-move
* final position is saved after drag completion

---

## Test 8: Corrupt JSON

Replace the workspace file with invalid JSON.

Restart.

Expected:

* Comma does not crash
* previous corrupted data is not blindly destroyed
* application starts with a safe workspace
* failure can be diagnosed

---

## Test 9: Missing Fields

Remove optional fields from a saved note.

Restart.

Expected:

* note loads
* safe defaults are applied

---

## Test 10: Invalid Position

Store a note at an inaccessible/off-screen position.

Restart.

Expected:

* note remains available
* note is moved to a safe visible position

---

## Test 11: Duplicate IDs

Create intentionally duplicated IDs.

Restart.

Expected:

* application does not crash
* duplicate identity is resolved
* resulting active notes have unique IDs

---

## Test 12: Schema Version

Load an older supported schema.

Expected:

```text id="q8n4m2"
old schema
   ↓
migration
   ↓
current schema
   ↓
workspace loads
```

---

# 36. Acceptance Criteria

Phase 6 is complete when:

* [ ] Workspace data has an explicit schema version.
* [ ] JSON storage implementation exists.
* [ ] Storage is isolated from the UI.
* [ ] Notes retain stable IDs across restarts.
* [ ] Titles persist.
* [ ] Content persists.
* [ ] Colors persist.
* [ ] Floating positions persist.
* [ ] Note dimensions persist.
* [ ] Dock state persists.
* [ ] Dock edge persists.
* [ ] Dock order persists.
* [ ] Workspace settings persist.
* [ ] Autosave exists.
* [ ] Text saving is debounced.
* [ ] Dragging does not trigger continuous disk writes.
* [ ] Shutdown performs a final save.
* [ ] Invalid geometry is safely recovered.
* [ ] Missing optional fields receive defaults.
* [ ] Duplicate IDs are handled safely.
* [ ] Missing workspace files are handled safely.
* [ ] Corrupted workspace files do not crash the application.
* [ ] Workspace writes are protected against partial-file corruption.
* [ ] Schema migration foundation exists.
* [ ] Runtime-only UI state is not persisted.
* [ ] Tests pass.

---

# 37. Phase 6 Definition of Done

The complete lifecycle should now be:

```text id="g6x1p8"
                 COMMA
                   │
              create/edit
                   │
                   ▼
             ┌───────────┐
             │   Notes   │
             └─────┬─────┘
                   │
            move / dock / reorder
                   │
                   ▼
             ┌───────────┐
             │ Workspace │
             └─────┬─────┘
                   │
                 save
                   │
                   ▼
              JSON Storage
                   │
                 quit
                   │
                 restart
                   │
                   ▼
              JSON Storage
                   │
                 load
                   │
                   ▼
             ┌───────────┐
             │ Workspace │
             └─────┬─────┘
                   │
              reconstruct
                   │
                   ▼
              Same Notes
              Same State
```

The architectural result is:

> **Comma now has memory.**

The desktop arrangement is no longer temporary application state. The workspace survives the lifetime of the process and can be reconstructed safely.

---

# 38. Phase Gate

Do not begin Phase 7 until Phase 6 passes its acceptance criteria.

The next phase will introduce:

> **Archive and Export**, giving users a deliberate way to retire notes without destroying them and to take note content outside Comma.
