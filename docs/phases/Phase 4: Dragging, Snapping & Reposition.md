# Phase 4: Dragging, Snapping & Repositioning

**Project:** Comma V2
**Phase:** 4
**Status:** Planned
**Primary Goal:** Allow users to intentionally move notes around the desktop and snap them back to the Comma edge dock.

---

# 1. Phase Objective

Phase 3 made notes reveal themselves through hover.

Phase 4 gives the user direct physical control over their position.

The core interaction becomes:

```text id="x1k4pf"
Docked
   ↓
Hover
   ↓
Expanded
   ↓
Grab header
   ↓
Drag
   ↓
Release
   ├── near edge → Dock
   └── elsewhere → Floating
```

The principle is:

> **If the user wants to move a note, Comma gets out of the way and lets them move it.**

---

# 2. What We Are Building

Phase 4 introduces:

* dragging expanded notes
* draggable note header
* pointer-offset preservation
* free desktop positioning
* edge proximity detection
* right-edge snapping
* dock/undock transitions caused by dragging
* drag-specific interaction state
* protection against hover collapse while dragging

---

# 3. Updated State Machine

The interaction model becomes:

```text id="y5xw8r"
                  ┌─────────────┐
                  │   DOCKED    │
                  └──────┬──────┘
                         │
                       hover
                         ▼
                  ┌─────────────┐
                  │  REVEALING  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  EXPANDED   │
                  └──────┬──────┘
                         │
                    drag begins
                         ▼
                  ┌─────────────┐
                  │  DRAGGING   │
                  └──────┬──────┘
                         │
                    release
                    ┌────┴────┐
                    ▼         ▼
              near edge    elsewhere
                    │         │
                    ▼         ▼
               DOCKING     FLOATING
                    │
                    ▼
                 DOCKED
```

The state machine must prevent unrelated automatic behaviors from interfering with an active drag.

---

# 4. Drag Initiation

The note should have a dedicated draggable header region.

Conceptually:

```text id="k9i8tu"
┌─────────────────────────────┐
│  ●  My Note              ⋯  │ ← draggable
├─────────────────────────────┤
│                             │
│  Note content...            │
│                             │
└─────────────────────────────┘
```

Dragging should begin from the header rather than the text-editing area.

This prevents accidental movement while selecting or typing text.

---

# 5. Pointer Offset Preservation

When dragging begins, Comma must remember where the pointer grabbed the note.

Example:

```text id="b4c6r2"
┌──────────────────┐
│       ●          │
│                  │
│                  │
└──────────────────┘
        ↑
     pointer
```

If the pointer grabbed the header 40 pixels from the left edge, the note should continue following that offset.

It must not jump so that its top-left corner suddenly moves underneath the cursor.

---

# 6. Dragging Behavior

During dragging:

```text id="p4t5f1"
mouse movement
      ↓
calculate desired position
      ↓
move NoteWindow
```

The movement should feel direct.

Do not introduce:

* delayed movement
* magnetic movement before release
* automatic rearrangement during the drag
* animation that fights the pointer

The pointer is authoritative during an active drag.

---

# 7. Dragging and Editing

The editor area must remain dedicated to editing.

Therefore:

```text id="w7s8r3"
Header      → drag
Content     → edit
Controls    → controls
```

Dragging should not begin simply because the user clicks inside the note.

This distinction is essential for a sticky-note application.

---

# 8. Dragging a Docked Note

A docked note must first become an interactive expanded note.

The intended flow is:

```text id="a9e3bc"
Docked
   ↓
Hover
   ↓
Expanded
   ↓
Grab header
   ↓
Dragging
```

Once dragging begins, the note is no longer constrained to its dock position.

Its docked state should become false during the drag.

---

# 9. Hover Collapse During Drag

Automatic collapse must be disabled while dragging.

This is mandatory.

Bad behavior:

```text id="0f5t7a"
drag
 ↓
mouse leaves
 ↓
collapse timer
 ↓
note disappears
```

Correct behavior:

```text id="0k4w9s"
drag
 ↓
mouse leaves original area
 ↓
note continues following pointer
```

The interaction priority established in Phase 3 remains:

```text id="h8k2mx"
Dragging
    >
Editing
    >
Explicit controls
    >
Hover
    >
Automatic collapse
```

---

# 10. Free Floating Position

If the user releases the note away from the edge:

```text id="9m7v2e"
Desktop

       ┌───────────────┐
       │     NOTE      │
       │               │
       └───────────────┘
```

the note should remain where the user placed it.

It becomes:

```text id="x3q7k9"
docked = false
```

The note is now a free-floating desktop note.

---

# 11. Edge Snap

If the user releases a note sufficiently close to the right edge:

```text id="7v1q6s"
                         cursor
                            ↓
┌───────────────────────────────────────────────┐
│                                  ┌─────────────┤
│                                  │    NOTE     │
└──────────────────────────────────┴─────────────┘
                                   ↑
                               near edge
```

Comma should snap it into the dock.

The final state becomes:

```text id="q5n8w4"
docked = true
edge = "right"
```

---

# 12. Snap Threshold

A configurable snap threshold should determine how close to the edge the note must be.

Conceptually:

```python id="d6m1yf"
if distance_to_right_edge <= SNAP_THRESHOLD:
    dock()
else:
    remain_floating()
```

The exact threshold is intentionally not finalized.

It should be centralized as configuration.

---

# 13. Snap Behavior

The snap itself may be animated.

For example:

```text id="u4w8z2"
release
  ↓
detect edge
  ↓
short snap animation
  ↓
docked position
```

The animation must be short enough that it feels like positioning assistance rather than an obstacle.

If animation introduces instability, correctness takes priority over visual smoothness.

---

# 14. Right Edge Only

Phase 4 continues to support only:

```text id="7s2m5r"
RIGHT EDGE
```

Do not implement:

* left edge snapping
* top edge snapping
* bottom edge snapping
* corner snapping

The data model may remain capable of representing other edges for future expansion.

The actual behavior remains right-edge-only.

---

# 15. Desktop Boundary Handling

Dragging must respect the available desktop environment.

The note should not accidentally become permanently unreachable because of invalid coordinates.

However, the user should still be able to position notes naturally near the edges.

Avoid excessive constraints.

Comma should prevent genuinely invalid/unrecoverable positioning, not police every pixel.

---

# 16. Docked Position After Dragging

When a note is snapped to the right edge, its vertical position should be derived from the user's release position.

For example:

```text id="8x2r5a"
User releases here
              ↓

┌───────────────────────────────────────────────┐
│                                               │
│                                               │
│                                  ┌────────────┤
│                                  │    NOTE    │
│                                  │            │
└──────────────────────────────────┴────────────┘
```

The note should dock at approximately that vertical location.

Phase 4 does **not** yet implement the final multi-note stacking algorithm.

---

# 17. Docked Note Ordering

The phase should record enough information to determine where a docked note currently sits vertically.

However, automatic ordering of multiple notes belongs to Phase 5.

For now:

* preserve the note's vertical position
* avoid overlapping where reasonably possible
* do not build a complex layout engine

---

# 18. Position Model

The persistent model already supports:

```text id="4r9n5p"
x
y
width
height
edge
docked
```

Phase 4 begins treating those values as meaningful workspace state.

For a floating note:

```text id="7s9w0q"
x = floating desktop position
y = floating desktop position
docked = false
```

For a docked note:

```text id="f8k3z1"
x = calculated dock position
y = dock vertical position
docked = true
edge = "right"
```

The exact persistence of these values remains part of the later persistence phase.

---

# 19. Interaction Ownership

Dragging should be implemented through the presentation/interaction layer.

`NoteWindow` can detect the mouse interaction.

Application-level positioning should be coordinated through the appropriate manager.

Conceptually:

```text id="q2k5m8"
Mouse Event
    ↓
NoteWindow
    ↓
Drag Interaction
    ↓
DockManager / positioning logic
    ↓
Note geometry
```

Avoid putting the complete docking algorithm inside mouse event handlers.

---

# 20. Drag Cancellation

The system should safely handle an interrupted drag.

Examples:

* application loses focus
* mouse interaction is interrupted
* window is destroyed
* user interaction is cancelled

The note must not become stuck in:

```text id="8c4n1p"
DRAGGING
```

A safe final position should always be established.

---

# 21. What Phase 4 Does NOT Do

## Multi-note Rearrangement

Not yet.

Dragging one note independently is the focus.

The final vertical dock stack and rearrangement behavior belongs to Phase 5.

---

## Hover Reveal Changes

Do not redesign the reveal interaction.

Phase 4 builds on Phase 3.

---

## Archive

Not yet.

---

## Export

Not yet.

---

## Full Persistence

Not yet.

Position data may update in memory, but complete restart restoration is a later phase.

---

## Advanced Docking

No multi-edge support.

No corner docking.

No workspace-aware multi-monitor docking system.

---

# 22. Testing

## Test 1: Basic Drag

1. Create a note.
2. Expand it.
3. Grab the header.
4. Move it around.
5. Release.

Expected:

* note follows pointer
* note does not jump at drag start
* note remains where released

---

## Test 2: Drag While Editing

1. Click inside content.
2. Select text.
3. Move the mouse.

Expected:

* text editing continues
* note does not unexpectedly move

---

## Test 3: Docked Note Drag

1. Dock a note.
2. Reveal it.
3. Grab its header.
4. Drag away.

Expected:

```text id="8q5r0p"
docked
  ↓
drag
  ↓
floating
```

---

## Test 4: Edge Snap

1. Drag a floating note toward the right edge.
2. Release within the snap threshold.

Expected:

```text id="v7x1w2"
floating
   ↓
release near edge
   ↓
snap
   ↓
docked
```

---

## Test 5: Outside Snap Threshold

1. Drag a note close to but outside the snap zone.
2. Release.

Expected:

* note remains floating
* no accidental docking occurs

---

## Test 6: Vertical Position

1. Drag a note to different vertical positions near the right edge.
2. Release.

Expected:

* note docks approximately where released
* its vertical position is preserved

---

## Test 7: Drag + Hover System

1. Reveal a docked note.
2. Start dragging.
3. Move outside the original note area.

Expected:

* note remains visible
* no collapse occurs
* note follows the pointer

---

## Test 8: Multiple Notes

Create three notes.

Move them independently.

Expected:

* dragging Note A does not move Note B or C
* each note maintains its own position/state

---

# 23. Acceptance Criteria

Phase 4 is complete when:

* [ ] Notes have a dedicated draggable header region.
* [ ] Users can drag expanded notes.
* [ ] Pointer offset is preserved.
* [ ] Notes move directly with the pointer.
* [ ] Editing content does not accidentally initiate dragging.
* [ ] Docked notes can be dragged away from the edge.
* [ ] Dragging disables automatic collapse.
* [ ] Notes can remain floating after release.
* [ ] Notes released near the right edge snap to the dock.
* [ ] Snap threshold is configurable.
* [ ] Right-edge snapping uses available desktop geometry.
* [ ] Dock state updates correctly after snapping.
* [ ] Vertical position is preserved when docking.
* [ ] Interrupted drags cannot leave notes in an invalid state.
* [ ] Multiple notes remain independently movable.
* [ ] No multi-note rearrangement system has been introduced.
* [ ] No archive/export system has been introduced.
* [ ] No full persistence system has been introduced.
* [ ] Tests pass.

---

# 24. Phase 4 Definition of Done

The complete interaction should now support:

```text id="w2n8j4"
                  ┌───────────┐
                  │   NOTE    │
                  └─────┬─────┘
                        │
                      hover
                        ↓
                  ┌───────────┐
                  │   NOTE    │
                  │           │
                  └─────┬─────┘
                        │
                     grab
                        ↓
                   ┌────────┐
                   │  NOTE  │
                   └────────┘
                        │
                      drag
                        ↓
              ┌──────────────────┐
              │     NOTE         │
              └──────────────────┘
                        │
                      release
                        ↓
                 near right edge?
                    /        \
                  yes         no
                   ↓           ↓
                Docked      Floating
```

The architectural result is:

> **The user now controls where a note lives on the desktop.**

Phase 5 will build on this by introducing **multiple-note dock arrangement and intentional vertical rearrangement**, turning individual docked notes into a coherent stack.
