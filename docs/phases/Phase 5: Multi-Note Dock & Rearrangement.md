# Phase 5: Multi-Note Dock & Rearrangement

**Project:** Comma V2
**Phase:** 5
**Status:** Planned
**Primary Goal:** Turn individually docked notes into an organized, vertically arranged dock that users can intentionally reorder.

---

# 1. Phase Objective

Phases 1 through 4 established:

```text
Independent notes
      ↓
Independent windows
      ↓
Edge docking
      ↓
Hover reveal
      ↓
Dragging
      ↓
Edge snapping
```

Phase 5 introduces the missing piece:

> **Multiple notes must understand that they share the same dock.**

Instead of allowing several notes to independently occupy arbitrary positions along the right edge, Comma will maintain a deterministic vertical arrangement.

Conceptually:

```text
┌───────────────────────────────────────────────┐
│                                      ┌───────┐│
│                                      │ Note A││
│                                      ├───────┤│
│                                      │ Note B││
│                                      ├───────┤│
│                                      │ Note C││
│                                      └───────┘│
└───────────────────────────────────────────────┘
```

The dock becomes a small, organized vertical neighborhood for notes.

---

# 2. Core Principle

The dock is not simply:

```text
"Put every note at x = screen_right"
```

It is a layout system.

The system must answer:

```text
Which notes are docked?
        ↓
What order are they in?
        ↓
Where should each note be vertically positioned?
        ↓
How should that position change when a note is rearranged?
```

That responsibility belongs to `DockManager`.

---

# 3. Scope

Phase 5 introduces:

* multi-note dock layout
* deterministic vertical ordering
* dock order
* automatic positioning
* dock spacing
* rearrangement of docked notes
* drag-to-reorder behavior
* insertion position calculation
* collision avoidance within the dock
* stable ordering after application events

---

# 4. Dock Layout

The initial dock remains:

```text id="u6p4sk"
RIGHT EDGE
```

Docked notes should occupy a vertical stack.

Example:

```text id="q7h3z9"
Desktop

                              ┌────────────┐
                              │   Note A   │
                              ├────────────┤
                              │   Note B   │
                              ├────────────┤
                              │   Note C   │
                              └────────────┘
```

The exact dimensions and spacing remain configurable.

---

# 5. Dock Order

Every docked note must have an explicit ordering value.

For example:

```text id="5y0s3d"
Note A → order 0
Note B → order 1
Note C → order 2
```

The order determines vertical placement.

The system must not depend on:

* window creation order alone
* Qt child-widget order
* object memory order
* dictionary iteration order
* current screen coordinates

Order is application state.

---

# 6. Layout Algorithm

The dock layout should follow a deterministic process.

Conceptually:

```text id="1k5m2r"
Get all docked notes
        ↓
Sort by order
        ↓
Calculate available dock area
        ↓
Place Note 1
        ↓
Place Note 2 below Note 1
        ↓
Place Note 3 below Note 2
        ↓
...
```

For example:

```text id="m4x7d1"
top
 ↓
┌────────────┐
│   Note A   │
└────────────┘
      gap
┌────────────┐
│   Note B   │
└────────────┘
      gap
┌────────────┐
│   Note C   │
└────────────┘
 ↓
bottom
```

---

# 7. Dock Spacing

A configurable gap should exist between notes.

Conceptually:

```python id="s6v3f8"
DOCK_SPACING = ...
```

The exact value is intentionally not finalized.

The important requirement is consistency.

There should not be arbitrary gaps created by individual notes.

---

# 8. Variable Note Heights

The layout should not assume every note has identical height.

For example:

```text id="g5p8w2"
┌────────────┐
│   Note A   │
│            │
└────────────┘

┌────────────┐
│   Note B   │
│            │
│            │
│            │
└────────────┘

┌────────────┐
│   Note C   │
└────────────┘
```

The next note's position should be calculated from the previous note's actual geometry.

Conceptually:

```text id="6y1n4k"
next_y = previous_y + previous_height + spacing
```

This prevents overlap when note sizes differ.

---

# 9. Available Dock Area

The dock should use the available desktop geometry.

The layout must account for:

* screen top
* screen bottom
* taskbar/system panel space
* note heights
* spacing

The system should never assume a fixed display resolution.

---

# 10. Overflow

A sufficiently large number of notes may exceed the available vertical screen space.

Phase 5 must define deterministic behavior for this situation.

The preferred initial behavior is:

> **Keep the dock within the available screen area as much as possible and avoid creating permanently unreachable notes.**

If all notes cannot fit simultaneously, the implementation may allow the stack to exceed the available height temporarily, but must preserve access to every note.

Do not introduce a dock scrollbar in this phase unless it becomes necessary.

---

# 11. Rearrangement

The user should be able to change the order of docked notes.

Example:

Initial:

```text id="d4s1z8"
Note A
Note B
Note C
```

User drags Note C above Note A:

```text id="y5n3m0"
Note C
Note A
Note B
```

The order values then become:

```text id="q9t4v6"
Note C → 0
Note A → 1
Note B → 2
```

The arrangement must be deterministic after the operation.

---

# 12. Rearrangement Interaction

The interaction should build on Phase 4.

The user grabs the note header:

```text id="v3w7q1"
┌─────────────────────┐
│  ●  Note A          │ ← grab
├─────────────────────┤
│                     │
│  content            │
└─────────────────────┘
```

and drags it vertically.

The dock should provide a clear indication of where the note will be inserted.

A temporary insertion position may be represented through:

* a gap
* placeholder
* positional movement of neighboring notes

The exact visual treatment can remain flexible.

---

# 13. Dragging a Docked Note

A docked note being dragged should behave differently from an ordinary floating note.

While the pointer remains within the dock:

```text id="x6m2b9"
drag vertically
     ↓
reorder
```

If the user pulls the note away from the edge:

```text id="e1j8r5"
drag away
     ↓
undock
     ↓
free floating
```

This preserves the behavior established in Phase 4.

---

# 14. Reordering Threshold

The dock should not reorder notes on every tiny pointer movement.

There should be an insertion threshold.

Conceptually:

```text id="r3q6z8"
Note A
────────────
Note B
────────────
Note C
```

When dragging Note C upward:

```text id="m1x7v2"
        ↑
      pointer
        │
    insertion
     threshold
```

Only when the pointer crosses the relevant midpoint/threshold should the note move in the ordering.

This prevents unstable rapid reordering.

---

# 15. Deterministic Ordering

The dock must always have one unambiguous order.

If two notes have the same position or ambiguous coordinates, order must still be determined using:

```text id="x9r4k2"
order
```

not raw pixel positions.

Coordinates are a consequence of the order.

They are not the source of truth for ordering.

---

# 16. DockManager Responsibilities

`DockManager` now becomes responsible for:

* finding docked notes
* sorting docked notes
* assigning vertical positions
* maintaining dock order
* calculating insertion positions
* updating order after rearrangement
* repositioning affected windows
* handling dock layout updates

It should not:

* modify note content
* render note UI
* manage text editing
* archive notes
* export notes
* persist directly to disk

---

# 17. NoteManager Responsibilities

`NoteManager` continues to own:

* note lifecycle
* creation
* removal
* lookup
* window association
* active-note collection

When a note is created or removed, `DockManager` may be asked to recalculate the dock layout.

Conceptually:

```text id="v8x2s1"
NoteManager
     │
     ├── create note
     │
     └── remove note
             │
             ▼
        DockManager
             │
             ▼
        re-layout dock
```

---

# 18. Dock Layout Updates

The dock should recalculate its layout when:

* a note becomes docked
* a note leaves the dock
* a note is reordered
* a docked note changes size
* a docked note is removed
* the screen geometry changes

The implementation should avoid unnecessary continuous layout recalculation.

---

# 19. Screen Resize

If the desktop geometry changes:

```text id="c8y4n1"
screen resize
     ↓
DockManager recalculates
     ↓
dock stack repositioned
```

Notes should remain associated with the right edge.

Do not permanently store screen-width-specific absolute dock coordinates.

---

# 20. Expanded Notes and the Dock

A docked note may be temporarily expanded through Phase 3's hover interaction.

Its expanded visual state should not permanently destroy the dock ordering.

For example:

```text id="z2x5m7"
Dock:

Note A
Note B
Note C


Hover Note B:

Note A
      ┌───────────────┐
      │    Note B     │
      │               │
      └───────────────┘
Note C
```

The underlying ordering remains:

```text id="y4k8s2"
A → 0
B → 1
C → 2
```

Reveal is a visual state.

It is not a reorder operation.

---

# 21. Rearrangement and Reveal

The system must distinguish:

```text id="f7n3c9"
Reveal
```

from:

```text id="p5r2w8"
Rearrange
```

Hovering a note must not change its dock order.

Dragging its header intentionally can change its order.

This distinction prevents accidental rearrangement.

---

# 22. Docked Note Identity

A note's position in the dock must never become its identity.

Incorrect:

```text id="h4q7m2"
Dock slot 1 = Note A
```

Correct:

```text id="w8k3z6"
Note ID = stable identity
order = current position
```

If Note A moves from first to third:

```text id="r6t1p9"
same Note ID
different order
```

No new note is created.

---

# 23. Removing a Docked Note

If a docked note is removed:

```text id="j2s5x8"
A
B
C

remove B

A
C
```

The remaining notes must be re-laid out.

Their order should become deterministic again.

For example:

```text id="c9v4m1"
A → 0
C → 1
```

There should be no permanent empty slot where Note B used to exist.

---

# 24. What Phase 5 Does NOT Do

## Archive

Not yet.

A note cannot be archived through this phase.

---

## Export

Not yet.

---

## Full Persistence

Not yet.

The ordering system should update runtime state correctly, but complete restart persistence remains Phase 6.

---

## Left/Top/Bottom Docks

Not yet.

Right-edge docking remains the only active dock.

---

## Advanced Overflow UI

No scrollable dock, pagination, or dock-management panel unless required by implementation.

---

## Visual Polish

Do not spend this phase on final animation curves, shadows, gradients, or decorative effects.

The ordering behavior comes first.

---

# 25. Testing

## Test 1: Two Notes

Create two docked notes.

Expected:

```text id="s4x8n1"
Note A
Note B
```

No overlap.

---

## Test 2: Three Notes

Create three notes.

Expected:

```text id="q1m7v5"
Note A
Note B
Note C
```

All notes have deterministic vertical positions.

---

## Test 3: Different Heights

Create notes with different heights.

Expected:

* no overlap
* spacing remains consistent
* each note's position is calculated from actual geometry

---

## Test 4: Reorder

Start with:

```text id="k5v8s2"
A
B
C
```

Drag C above A.

Expected:

```text id="r7x1p4"
C
A
B
```

Order values update correctly.

---

## Test 5: Reorder Repeatedly

Move notes:

```text id="y4z8n3"
A B C
↓
C A B
↓
B C A
↓
A B C
```

Expected:

* no duplicate order values
* no missing order values
* no unstable positions

---

## Test 6: Remove Note

Start:

```text id="d8m2q5"
A
B
C
```

Remove B.

Expected:

```text id="p3v7x1"
A
C
```

The stack closes the gap.

---

## Test 7: Dock New Note

Existing:

```text id="f5w8k2"
A
B
```

Dock C.

Expected:

```text id="r2n6m9"
A
B
C
```

The new note receives a deterministic position.

---

## Test 8: Undock Middle Note

Start:

```text id="u3q7y5"
A
B
C
```

Undock B.

Expected:

```text id="z8m4p1"
A
C
```

No empty slot remains.

---

## Test 9: Pull Docked Note Away

Drag B away from the right edge.

Expected:

```text id="k9x2s6"
A
C

B → floating
```

The dock automatically reflows.

---

## Test 10: Screen Resize

Resize or change the available desktop geometry.

Expected:

* dock remains attached to the right edge
* stack recalculates
* notes remain accessible

---

# 26. Acceptance Criteria

Phase 5 is complete when:

* [ ] Multiple docked notes form a deterministic vertical stack.
* [ ] Every docked note has an explicit order.
* [ ] Dock layout uses note geometry rather than fixed-height assumptions.
* [ ] Configurable spacing exists between notes.
* [ ] Docked notes do not unintentionally overlap.
* [ ] Users can vertically rearrange docked notes.
* [ ] Dragging a docked note can change its order.
* [ ] Reordering uses an intentional insertion threshold.
* [ ] Pulling a docked note away from the edge still supports Phase 4 floating behavior.
* [ ] Removing a note causes the dock to reflow.
* [ ] Docking a new note causes the dock to reflow.
* [ ] Undocking a note causes the dock to reflow.
* [ ] Reveal does not accidentally change dock order.
* [ ] Note identity remains independent of dock position.
* [ ] Screen geometry changes trigger a correct re-layout.
* [ ] Order remains deterministic after repeated rearrangement.
* [ ] No archive/export functionality has been introduced.
* [ ] No full persistence implementation has been introduced.
* [ ] Tests pass.

---

# 27. Phase 5 Definition of Done

The intended result is:

```text
                     COMMA DOCK

                         ┌─────────────┐
                         │   NOTE C    │
                         ├─────────────┤
                         │   NOTE A    │
                         ├─────────────┤
                         │   NOTE B    │
                         └─────────────┘
                               │
                            right edge
```

The user can:

```text
Create
  ↓
Dock
  ↓
Reveal
  ↓
Grab
  ↓
Drag vertically
  ↓
Choose a new position
  ↓
Release
  ↓
Dock reorganizes
```

The architectural result is:

> **The dock is now a real layout system rather than a collection of independently positioned windows.**

This is the point where Comma starts behaving like the reference concept at the multi-note level.

---

# 28. Phase Gate

Do not begin Phase 6 until Phase 5 passes its acceptance criteria.

The next phase will introduce:

> **Complete workspace persistence and restoration.**

That means Comma will finally remember where its notes are, which notes are docked, their order, their dimensions, and their state across application restarts.
