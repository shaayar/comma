# Phase 2: Edge Docking

**Project:** Comma V2
**Phase:** 2
**Status:** Planned
**Primary Goal:** Introduce persistent desktop-edge docking for independent notes.

---

## 1. Phase Objective

Give Comma notes their first defining desktop behavior:

> **A note can attach itself to the edge of the desktop and occupy only a small visible portion of the screen.**

The initial supported edge is:

```text
RIGHT EDGE
```

A docked note should no longer behave like an ordinary floating window.

Conceptually:

```text
Desktop
┌───────────────────────────────────────────────┐
│                                               │
│                                               │
│                                               │████
│                                               │████
│                                               │████
└───────────────────────────────────────────────┘
                                                ↑
                                           docked note
```

The visible portion acts as the note's presence on the desktop.

---

# 2. What We Are Building

Phase 2 introduces:

* right-edge docking
* undocked → docked transition
* docked → undocked positioning
* partial note visibility
* edge-position calculation
* a dedicated `DockManager`
* separation between note data and dock geometry

The note itself remains the same `Note`.

We are changing **where and how the window is positioned**, not what the note is.

---

# 3. Architecture

The architecture becomes:

```text
                     AppController
                           │
                           ▼
                     NoteManager
                           │
              ┌────────────┴────────────┐
              │                         │
          Note Model                DockManager
              │                         │
              └──────────┬──────────────┘
                         ▼
                    NoteWindow
```

`DockManager` owns docking calculations.

`NoteManager` owns note lifecycle.

`NoteWindow` renders and interacts with the user.

---

# 4. Docked State

A note must have two meaningful positional states:

```text
UNDPCKED
DOCKED
```

Conceptually:

```text
             ┌───────────────┐
             │     Note      │
             │               │
             │   floating    │
             └───────────────┘


                    ↓ dock


┌───────────────────────────────────────────────┐
│                                               │
│                                      ┌────────┤
│                                      │  Note  │
│                                      │        │
└──────────────────────────────────────┴────────┘
```

When docked, the window remains a real window.

It is not converted into a widget inside a central application window.

---

# 5. Right Edge

The right side of the available desktop area is the first supported docking edge.

For a right-edge dock:

```text
screen_right = available_geometry.right()
```

The note should be positioned so that its right boundary aligns with the desktop's right boundary.

A portion of the note remains visible.

The rest extends beyond the visible desktop area.

---

# 6. Dock Tab / Visible Sliver

A docked note should expose a configurable visible width.

For example:

```text
┌───────────────────────────────────────────────┐
│                                               │
│                                      ┌────────┤
│                                      │        │
│                                      │  tab   │
│                                      │        │
└──────────────────────────────────────┴────────┘
```

The exact width is **not finalized in Phase 2**.

It should be represented as a configurable value rather than scattered as hard-coded numbers.

Example concept:

```python
DOCK_VISIBLE_WIDTH = ...
```

The final value can be tuned during visual-polish work.

---

# 7. DockManager Responsibilities

Create:

```text
application/dock_manager.py
```

`DockManager` is responsible for:

* determining the available desktop geometry
* calculating dock positions
* docking a note window
* undocking a note window
* determining whether a window is docked
* calculating the visible dock region
* maintaining the conceptual dock state

It should **not**:

* own note content
* edit note text
* save notes
* render note UI
* implement hover animation
* implement dragging
* decide archive behavior

Those belong elsewhere.

---

# 8. Docking API

The implementation should expose a small, predictable interface.

Conceptually:

```python
dock_manager.dock(note_window)
dock_manager.undock(note_window)
dock_manager.is_docked(note_id)
```

The exact implementation may differ.

The important requirement is that docking is a distinct application-level operation rather than scattered coordinate manipulation inside `NoteWindow`.

---

# 9. Note Model Changes

The `Note` model should now be capable of representing docking state.

Add:

```text
edge
docked
```

Potentially:

```text
edge = "right"
docked = true
```

These values describe persistent workspace state.

However, Phase 2 does not yet require complete workspace persistence.

The model should therefore be ready for persistence without making persistence the focus of this phase.

---

# 10. Positioning Rules

When a note is docked:

```text
right edge of NoteWindow
        =
right edge of available desktop
```

The note should remain vertically positioned according to its current position.

For example:

```text
Before docking:

      ┌──────────────┐
      │              │
      │     Note     │
      │              │
      └──────────────┘


After docking:

┌───────────────────────────────────────────────┐
│                                      ┌────────┤
│                                      │        │
│                                      │  Note  │
│                                      │        │
└──────────────────────────────────────┴────────┘
```

Phase 2 does **not** yet determine the final vertical arrangement of multiple docked notes.

---

# 11. Undocking

A docked note must be capable of becoming a normal floating note again.

When undocked:

```text
docked
  ↓
restore floating geometry
```

The window should return to a usable desktop position.

The exact trigger for undocking is intentionally deferred to Phase 3.

For Phase 2, the operation may be triggered through a temporary development control.

This is important:

> Phase 2 builds the docking mechanism. Phase 3 decides how users naturally trigger it.

---

# 12. Geometry Preservation

Docking should not destroy the note's normal dimensions.

If a note is:

```text
width  = 300
height = 250
```

docking should not permanently turn it into a 40-pixel-wide note.

Instead:

```text
Normal geometry
      ↓
temporarily positioned outside screen
      ↓
visible dock region
```

The underlying window dimensions remain available for later reveal behavior.

This will make Phase 3's animated reveal possible without redesigning the window.

---

# 13. Desktop Geometry

Use the desktop's **available screen geometry**, not arbitrary hard-coded screen dimensions.

The implementation must account for desktop boundaries such as:

* taskbars
* system panels
* available work area

The code should use Qt's screen/desktop geometry APIs.

Do not assume:

```text
1920 × 1080
```

or any other fixed resolution.

---

# 14. Multiple Screens

Phase 2 should avoid introducing monitor-specific complexity.

The initial implementation should work correctly on the primary available screen.

The architecture should not prevent future multi-monitor support.

Do not introduce:

* monitor IDs
* complex monitor persistence
* monitor-specific workspace management
* cross-monitor docking rules

unless required to make the basic docking behavior work.

---

# 15. Always-On-Top Behavior

Docked notes should retain Comma's desktop-note nature.

If always-on-top behavior was established in Phase 1, docking must not accidentally remove it.

However, do not introduce a complicated window-management system here.

The requirement is simply:

> Docking must preserve the existing note-window behavior.

---

# 16. What Phase 2 Does NOT Do

The following are explicitly excluded.

## Hover Reveal

Not yet.

There should be no:

```text
hover
  ↓
slide inward
```

That is Phase 3.

---

## Animation

No animated movement.

Docking can happen instantly during this phase.

---

## Dragging

No drag-to-dock.

No drag-to-rearrange.

No drag thresholds.

---

## Automatic Rearrangement

If multiple notes are docked:

```text
████
████
████
```

Phase 2 does not decide their final stacking algorithm.

---

## Hover Detection

No special hover state machine.

No mouse-leave collapse behavior.

---

## Archive

Not yet.

---

## Export

Not yet.

---

# 17. Temporary Development Controls

Because the final user interaction is intentionally deferred, Phase 2 may use temporary controls such as:

```text
[ Dock ]
[ Undock ]
```

or keyboard shortcuts.

These controls are strictly development mechanisms.

They are not necessarily part of the final Comma interface.

They may be removed once Phase 3 introduces the proper interaction model.

---

# 18. Testing

## Test 1: Dock

Create a note and invoke the dock operation.

Expected:

* note moves to the right desktop edge
* right edge aligns with available screen boundary
* only the configured dock region remains visible

---

## Test 2: Undock

Dock a note, then invoke undock.

Expected:

* note becomes a normal floating window
* note content remains unchanged
* note dimensions remain unchanged

---

## Test 3: Multiple Notes

Create several notes and dock them.

Expected:

* each note can independently enter docked state
* docking one note does not destroy another
* note IDs remain stable

---

## Test 4: Different Screen Sizes

Test on at least two different window/screen resolutions.

Expected:

* dock position is calculated dynamically
* no hard-coded screen resolution is required

---

## Test 5: Content Preservation

Dock a note containing text.

Undock it.

Expected:

```text
content_before == content_after
```

---

## Test 6: Window Identity

Dock and undock a note.

Expected:

* the same `Note` remains associated with the window
* no duplicate note is created
* no note data is lost

---

# 19. Acceptance Criteria

Phase 2 is complete when:

* [ ] `DockManager` exists.
* [ ] Right-edge docking works.
* [ ] Dock position uses available desktop geometry.
* [ ] Docked notes partially extend beyond the desktop.
* [ ] A configurable visible dock width exists.
* [ ] Notes can be docked independently.
* [ ] Notes can be undocked.
* [ ] Note content survives docking/undocking.
* [ ] Note dimensions are not destroyed by docking.
* [ ] Docking state is represented separately from note content.
* [ ] `NoteWindow` does not contain the global docking algorithm.
* [ ] Multiple docked notes can coexist.
* [ ] No hover reveal has been implemented.
* [ ] No animation has been implemented.
* [ ] No drag/snap system has been implemented.
* [ ] No archive/export system has been implemented.
* [ ] Tests pass.

---

# 20. Phase 2 Definition of Done

The phase succeeds when Comma can reliably perform:

```text
Create Note
     ↓
Floating Note
     ↓
Dock Right
     ↓
Partially Hidden Desktop Note
     ↓
Undock
     ↓
Floating Note
```

The important architectural result is:

> **Comma now understands the difference between a floating note and a docked note.**

Phase 3 can then turn this mechanical docking capability into the reference interaction:

```text
Hover
  ↓
Reveal
  ↓
Edit
  ↓
Leave
  ↓
Collapse
```

No Phase 3 interaction should be added before this docking foundation is stable.
