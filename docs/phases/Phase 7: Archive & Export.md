# Phase 7: Archive & Export

**Project:** Comma V2
**Phase:** 7
**Status:** Planned
**Primary Goal:** Introduce non-destructive note archiving and user-controlled note export.

---

# 1. Phase Objective

Up to Phase 6, Comma can create, edit, move, dock, rearrange, and remember notes.

Phase 7 introduces lifecycle management.

The user must now be able to say:

```text
"I don't need this note on my desktop anymore."
```

without meaning:

```text
"Delete this note forever."
```

Therefore Comma gains:

```text
Archive
```

and:

```text
Export
```

The core principle is:

> **Removing a note from the active desktop should not automatically destroy it.**

---

# 2. What We Are Building

Phase 7 introduces:

* archive action
* archived note state
* removing archived notes from active desktop presentation
* archive restoration
* archived-note access
* export action
* plain-text export
* user-selected export location
* export error handling
* separation between archive and delete

---

# 3. Note Lifecycle

The lifecycle becomes:

```text id="x8k3p2"
             ┌──────────────┐
             │ Active Note  │
             └──────┬───────┘
                    │
                 archive
                    ↓
             ┌──────────────┐
             │   Archived   │
             └──────┬───────┘
                    │
                 restore
                    ↓
             ┌──────────────┐
             │ Active Note  │
             └──────────────┘
```

Export is independent:

```text id="q4m7v1"
Active / Archived
       │
       │ export
       ▼
  External File
```

Export must not modify the note's lifecycle state.

---

# 4. Archive Semantics

Archiving means:

> **Remove this note from the active desktop workspace while preserving the note and its data.**

When archived:

```text id="f6n2r8"
archived = true
```

The note remains part of the workspace data.

It should not be treated as deleted.

---

# 5. What Happens to the Window

When a note is archived:

```text id="s3v8k5"
Active Note
    ↓
archive
    ↓
destroy/hide NoteWindow
    ↓
Note remains in NoteManager/workspace
```

The exact window lifecycle can be implementation-specific.

The important invariant is:

```text id="m7x1q4"
window disappears
       ≠
note disappears
```

---

# 6. Archived Notes Must Not Participate in the Dock

If:

```text id="r5p8c2"
Note A → active
Note B → archived
Note C → active
```

the dock should behave as:

```text id="n2k6v9"
Note A
Note C
```

Note B must not occupy a visible dock slot.

The dock layout should ignore archived notes.

---

# 7. Dock Reflow

Archiving a docked note must trigger the same kind of layout update as removing an active note.

Before:

```text id="h4q9m1"
A
B
C
```

Archive B:

```text id="z7x2p5"
A
C
```

The dock must close the gap.

---

# 8. Floating Notes

Archiving a floating note should also remove its window from the active desktop.

The underlying note remains preserved.

When restored, the note should return using its stored workspace state where possible.

---

# 9. Restoring an Archived Note

The user must have a way to access archived notes.

The archive system should support:

```text id="y5n8k3"
Archived Notes
     ↓
select note
     ↓
Restore
     ↓
Active Note
```

When restored:

```text id="v2r6m9"
archived = false
```

The note should become active again.

---

# 10. Archive Access UI

A dedicated archive interface should be introduced.

The exact final UI is intentionally flexible.

Possible implementation:

```text id="x9m4q7"
┌─────────────────────────────┐
│ Archived Notes               │
├─────────────────────────────┤
│ Meeting Ideas                │
│ Shopping                    │
│ Project Notes               │
├─────────────────────────────┤
│ [Restore] [Export]          │
└─────────────────────────────┘
```

This does **not** need to become a permanent large application window.

The UI should remain consistent with Comma's lightweight desktop philosophy.

---

# 11. Archive Interaction

Archive should be accessible from an explicit note control.

For example:

```text id="q7w3m8"
┌──────────────────────────┐
│ ●  My Note          ⋯    │
├──────────────────────────┤
│                          │
│ Content                  │
│                          │
├──────────────────────────┤
│        Archive           │
└──────────────────────────┘
```

The exact icon/control is not finalized.

The action itself must be explicit.

Do not archive notes simply because they collapse.

---

# 12. Collapse vs Archive

These behaviors must remain completely separate.

```text id="t4n8p2"
Mouse leaves
    ↓
Collapse
    ↓
Note remains active
```

versus:

```text id="c6x1m9"
User chooses Archive
    ↓
Note leaves active workspace
    ↓
Note remains stored
```

A collapsed note is still active.

An archived note is not.

---

# 13. Archive vs Delete

The system must clearly distinguish:

```text id="j8r3v5"
Archive
```

from:

```text id="p4m7x2"
Delete
```

Archive:

```text id="d5n9q1"
reversible
preserves data
removes from desktop
```

Delete:

```text id="w2x6k8"
destructive
removes note permanently
```

If a destructive delete action already exists in the codebase, it must not be renamed internally to archive.

The semantics must be correct.

---

# 14. Delete

A permanent delete operation is allowed to exist in this phase if needed.

However, it must be explicit.

For example:

```text id="m3q7v1"
Archive
Delete permanently
```

Delete should not happen accidentally through:

* closing a window
* collapsing a note
* dragging it away
* restarting Comma

If permanent deletion is implemented, a confirmation step should be considered for notes containing content.

---

# 15. Archive Persistence

Phase 6 already introduced:

```text id="r8n2v5"
archived
```

Phase 7 now gives this field real user-facing meaning.

When archived:

```text id="f3m9q6"
archived = true
```

must be persisted.

After restart:

```text id="k7x4p1"
archived = true
```

must still be true.

Archived notes must not unexpectedly reappear on the desktop.

---

# 16. Restore Persistence

If a user restores an archived note:

```text id="v9m2c5"
archived = false
```

that state must be saved.

After restart, the note remains active.

---

# 17. Restored Position

When restoring an archived note:

* if its previous floating position is valid, restore it
* if its previous dock state was valid, restore it according to the current dock rules
* if the old geometry is invalid, use safe positioning

The archive operation should not destroy the note's previous geometry.

For example:

```text id="p6x1r8"
Before archive:

Floating
x = 700
y = 300

Archive
   ↓

Restore
   ↓

Floating
x = 700
y = 300
```

---

# 18. Export

The export system allows the user to take note content outside Comma.

Initial export format:

```text id="q2n7m4"
Plain Text (.txt)
```

This keeps the feature simple and reliable.

---

# 19. Export Contents

A basic text export should contain:

```text id="w5r8k3"
Note Title

Note content...
```

For example:

```text id="a4v9x2"
Shopping List

Milk
Bread
Eggs
```

The exact formatting can evolve later.

The exported file should contain the useful user-facing content, not internal application metadata.

Do not export:

```text id="s7m1q6"
note ID
x/y coordinates
dock state
order
animation state
internal settings
```

unless a future dedicated workspace-export feature explicitly requires it.

---

# 20. Export Filename

The default filename should be derived from the note title.

For example:

```text id="k3x8m5"
"My Shopping List"
        ↓
"My Shopping List.txt"
```

The implementation must sanitize characters that are invalid in filenames on the current platform.

If the title is empty:

```text id="r9q2v6"
Untitled.txt
```

may be used.

---

# 21. Export Location

The user should choose the export location through the operating system's standard file-save dialog.

Conceptually:

```text id="m8p3x7"
Export
  ↓
Save dialog
  ↓
user selects location
  ↓
write .txt
```

Do not silently place exports in an arbitrary application directory.

---

# 22. Exporting Archived Notes

Archived notes must also be exportable.

The export action should operate on the `Note` model.

Therefore:

```text id="y6v1q4"
Active Note
   ↓
Export

Archived Note
   ↓
Export
```

both use the same export service.

---

# 23. Export Must Not Modify the Note

After export:

```text id="n4x8m2"
content unchanged
title unchanged
archived unchanged
position unchanged
dock state unchanged
```

Export is a read operation against the note's data.

---

# 24. Export Service

Introduce an infrastructure-level export service.

Conceptually:

```text id="p7q2k9"
infrastructure/
    export.py
```

The presentation layer requests an export.

It should not construct raw file-writing logic itself.

For example:

```python id="v3m8x1"
exporter.export_note(note, destination)
```

The exact API can differ.

---

# 25. Export Errors

Possible failures include:

* invalid destination
* permission denied
* disk full
* file already inaccessible
* user cancels dialog

Comma should handle these without crashing.

If the user cancels:

```text id="c8r4m2"
Export cancelled
```

This is not an error.

If writing fails:

```text id="x5n9q7"
Export failed
```

the user should receive a clear explanation.

---

# 26. Archive Window / Archive View

The archive view should display enough information for the user to identify notes.

At minimum:

```text id="m1q6v8"
Title
```

Optionally:

```text id="r7x3k2"
last modified
preview
color
```

Do not turn the archive into a complicated database browser.

The feature should remain lightweight.

---

# 27. Archive Search

Search is **not required** in Phase 7.

If the number of archived notes makes search necessary later, it can become a future feature.

Do not build a search engine merely because an archive list exists.

---

# 28. Archive Sorting

Archived notes should have deterministic ordering.

A simple initial ordering can be:

```text id="z4p8m1"
most recently archived
```

or another explicitly chosen rule.

The exact ordering should be finalized during implementation.

The important requirement is that the list should not appear randomly reordered between openings.

---

# 29. NoteManager Responsibilities

`NoteManager` now handles:

* archive note
* restore note
* retrieve active notes
* retrieve archived notes
* remove archived note permanently if delete exists
* notify relevant systems about lifecycle changes

Conceptually:

```text id="g5x2r9"
manager.archive(note_id)
manager.restore(note_id)
manager.get_active_notes()
manager.get_archived_notes()
```

---

# 30. DockManager Responsibilities

When a note is archived:

```text id="p3k7v2"
DockManager
    ↓
remove note from active dock layout
    ↓
recalculate stack
```

When restored:

```text id="x8m4q1"
DockManager
    ↓
determine restored dock state
    ↓
insert note into layout
    ↓
recalculate stack
```

---

# 31. Persistence Responsibilities

The persistence system must save:

```text id="n7q2c5"
archived = true/false
```

and all relevant note state.

Archive and restore should trigger the existing debounced persistence mechanism from Phase 6.

---

# 32. What Phase 7 Does NOT Do

## Cloud Archive

No cloud storage.

---

## Trash / Recovery System

No sophisticated trash system.

Archive is sufficient for reversible removal.

---

## Rich Export

No:

* PDF export
* Markdown export
* HTML export
* Word documents
* images

The initial export format is plain text.

---

## Bulk Export

No exporting every note simultaneously.

Single-note export is the initial requirement.

---

## Search

No archive search.

---

## Tags

No tagging or categorization system.

---

## Advanced Archive Management

No:

* archive folders
* archive categories
* archive pinning
* archive sharing
* archive synchronization

---

# 33. Testing

## Test 1: Archive Active Note

1. Create a note.
2. Add content.
3. Archive it.

Expected:

* note disappears from active desktop
* note remains in workspace
* note appears in archived collection

---

## Test 2: Archive Docked Note

1. Dock a note.
2. Archive it.

Expected:

* note disappears from dock
* dock reflows
* note remains recoverable

---

## Test 3: Archive Floating Note

1. Move note to a floating position.
2. Archive it.

Expected:

* note window disappears
* note remains archived

---

## Test 4: Restore

1. Archive a note.
2. Open archived notes.
3. Restore it.

Expected:

* note becomes active
* note window returns
* content is unchanged

---

## Test 5: Restore Docked Note

Archive a previously docked note.

Restore it.

Expected:

* its previous dock state is respected
* dock layout updates correctly

---

## Test 6: Restart While Archived

1. Archive a note.
2. Quit Comma.
3. Restart.

Expected:

* note remains archived
* note does not unexpectedly appear on desktop

---

## Test 7: Restart After Restore

1. Restore archived note.
2. Quit.
3. Restart.

Expected:

* note remains active

---

## Test 8: Export Active Note

1. Create note.
2. Add title/content.
3. Export as `.txt`.

Expected:

* file is created
* title is present
* content is present
* internal metadata is absent

---

## Test 9: Export Archived Note

Export an archived note.

Expected:

* export succeeds
* note remains archived

---

## Test 10: Export Does Not Mutate

Before export:

```text id="q8m3v5"
note state = X
```

After export:

```text id="k1r7p2"
note state = X
```

No state changes.

---

## Test 11: Cancel Export

Open export dialog and cancel.

Expected:

* no file is created
* application remains stable
* note remains unchanged

---

## Test 12: Export Failure

Attempt export to an invalid/unwritable location.

Expected:

* application does not crash
* user receives an error
* note remains unchanged

---

# 34. Acceptance Criteria

Phase 7 is complete when:

* [ ] Notes can be archived explicitly.
* [ ] Archiving removes the note from the active desktop.
* [ ] Archived notes remain stored.
* [ ] Archived notes do not participate in dock layout.
* [ ] Dock reflows after archiving.
* [ ] Archived notes can be viewed.
* [ ] Archived notes can be restored.
* [ ] Restore returns the note to the active workspace.
* [ ] Previous valid geometry/state is preserved where appropriate.
* [ ] Archive state persists across restart.
* [ ] Restore state persists across restart.
* [ ] Active notes can be exported.
* [ ] Archived notes can be exported.
* [ ] Plain-text `.txt` export works.
* [ ] Export filename is derived safely from the title.
* [ ] User chooses the export location.
* [ ] Export does not mutate note state.
* [ ] Export failures are handled safely.
* [ ] Archive and collapse remain distinct behaviors.
* [ ] Archive and delete remain distinct semantics.
* [ ] No cloud/archive synchronization has been introduced.
* [ ] No advanced export formats have been introduced.
* [ ] Tests pass.

---

# 35. Phase 7 Definition of Done

The complete lifecycle is now:

```text id="x3k7m9"
                 ┌─────────────┐
                 │ Active Note │
                 └──────┬──────┘
                        │
             ┌──────────┴──────────┐
             │                     │
          Archive                Export
             │                     │
             ▼                     ▼
      ┌─────────────┐        ┌──────────┐
      │  Archived   │        │  .txt    │
      │    Note     │        │   File   │
      └──────┬──────┘        └──────────┘
             │
          Restore
             │
             ▼
      ┌─────────────┐
      │ Active Note │
      └─────────────┘
```

The architectural result is:

> **Comma can now manage the full active-to-archived lifecycle without confusing hiding, archiving, exporting, and deletion.**

---

# 36. Phase Gate

Do not begin Phase 8 until Phase 7 passes its acceptance criteria.

The next phase will focus on:

> **Visual polish and reference-level interaction refinement.**

That is where we tune the personality of Comma: note appearance, colors, shadows, typography, controls, spacing, animation feel, and the final desktop experience.
