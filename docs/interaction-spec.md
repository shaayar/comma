# Comma V2

## Interaction Specification

**Status:** Draft
**Version:** 2.0
**Parent:** `COMMA_V2.md`
**Related:** `architecture.md`

---

# 1. Purpose

This document defines how Comma V2 should behave from the user's perspective.

It converts the reference implementation into explicit interaction rules so that implementation decisions do not depend on subjective interpretation.

The primary reference behavior is:

```text
Notes live on screen edge
        ↓
User hovers/interacts
        ↓
Note reveals itself
        ↓
User reads / edits / moves it
        ↓
User leaves it
        ↓
Note returns to edge
```

---

# 2. Reference Interaction

The reference demonstrates the following core behavior:

* Multiple notes exist simultaneously.
* Notes are attached to the right edge of the screen.
* Each note has a distinct color.
* Docked notes expose only a small visible portion.
* Hovering reveals a note.
* Expanded notes can be edited.
* Notes can be moved/rearranged.
* Notes can be archived or exported.
* Multiple docked notes are vertically arranged along the edge.

These behaviors form the baseline for Comma V2.

---

# 3. Interaction Vocabulary

Comma uses the following terms.

### Note

A persistent piece of user information.

### Docked

A note is attached to a screen edge and mostly hidden.

### Expanded

A note is fully visible on the desktop.

### Tab

The visible portion of a docked note.

### Active note

A note currently being interacted with.

### Rearranging

Changing the order or position of notes along the dock.

### Workspace

The complete collection of active and archived notes.

---

# 4. Default Dock

The initial default dock is:

```text
RIGHT EDGE
```

Example:

```text
┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│                                             │
│                                      ┌──────┤
│                                      │ Note │
│                                      ├──────┤
│                                      │ Note │
│                                      ├──────┤
│                                      │ Note │
│                                      └──────┤
└─────────────────────────────────────────────┘
```

Left, top and bottom docking are architectural extension points but are not required for the initial interaction implementation.

---

# 5. Docked Note

A docked note must:

* remain partially visible
* remain clickable/hoverable
* occupy minimal desktop space
* retain its color identity
* retain its position/order
* remain above normal application windows where configured

A docked note is not considered closed.

It remains fully active.

---

# 6. Docked Tab

The visible portion of the note is called the **tab**.

The tab should provide enough visual information for the user to identify that something is present.

The tab may expose:

* note color
* a small title/label
* a visual handle

It should not expose the entire note content.

The exact dimensions will be defined during visual implementation.

---

# 7. Hover-to-Reveal

The primary reveal mechanism is hover.

```text
Mouse
  │
  ▼
Docked tab
  │
  ▼
Hover detected
  │
  ▼
Expand
```

The note should begin revealing itself after the pointer enters the interactive tab region.

The system should not require a precise click for basic reading.

---

# 8. Reveal Direction

For the default right-side dock:

```text
                 DESKTOP

                  ┌───────────────┐
                  │     NOTE      │
                  │               │
                  └───────────────┘
                              ▲
                              │
                         expands
                              │
                         RIGHT EDGE
```

The note expands **inward**, toward the center of the desktop.

It must not expand outward beyond the screen.

For future edges:

```text
RIGHT → expand left
LEFT  → expand right
TOP   → expand down
BOTTOM → expand up
```

---

# 9. Reveal Animation

Expansion must be animated.

The visual motion should communicate:

> "This note is coming out from the edge."

It should not simply appear at full size.

Conceptually:

```text
DOCKED
┌────┐
│    │
└────┘
   ↓
  ┌──────────┐
  │          │
  └──────────┘
       ↓
┌────────────────┐
│                │
│      NOTE      │
│                │
└────────────────┘
```

The animation should be:

* short
* smooth
* predictable
* interruptible

Exact duration should be tuned against the reference during implementation.

---

# 10. Expanded Note

An expanded note is a normal interactive desktop surface.

The user can:

* read content
* edit content
* drag the note
* change appearance
* archive it
* export it
* access secondary actions

The note remains associated with its original dock position.

---

# 11. Expanded Geometry

The note should have a consistent default size.

Example:

```text
┌──────────────────────────────┐
│ Title                    ··· │
├──────────────────────────────┤
│                              │
│ Note content                 │
│                              │
│                              │
│                              │
├──────────────────────────────┤
│ ● ● ●     Archive    Export  │
└──────────────────────────────┘
```

The exact width/height is a visual design decision.

The architecture must allow the user to resize notes in the future.

Resizable notes are not required for the initial implementation.

---

# 12. Editing

The content area is directly editable.

When the user clicks inside the content:

```text
NOTE
  ↓
Editor receives focus
  ↓
Keyboard input
  ↓
Content changes
```

There is no mandatory separate "Edit" button.

---

# 13. Text Persistence

Content changes should not require the user to manually save.

The system should persist changes automatically.

Recommended behavior:

```text
User types
    ↓
Content changed
    ↓
Debounced save
    ↓
Storage
```

The exact debounce interval belongs to implementation.

---

# 14. Focus

An expanded note receiving focus should become the active note.

The active note should visually communicate focus subtly.

When another note is selected:

```text
Note A active
      ↓
User interacts with Note B
      ↓
Note B active
      ↓
Note A inactive
```

Only one note should be the primary keyboard focus target at a time.

---

# 15. Mouse Leave

Leaving an expanded note should normally begin the collapse process.

However, the note must **not immediately collapse** on every mouse-leave event.

The implementation must account for:

* pointer movement
* animation
* dragging
* editing
* controls
* pointer travel toward the dock

A short collapse delay is expected.

---

# 16. Collapse Conditions

A note may collapse when:

```text
Mouse leaves note
AND
not dragging
AND
not actively interacting
AND
not focused through an interaction that requires persistence
```

Then:

```text
EXPANDED
   ↓
collapse delay
   ↓
COLLAPSING
   ↓
DOCKED
```

---

# 17. Collapse Delay

A short delay should exist between mouse exit and collapse.

Purpose:

* prevent accidental collapse
* allow the user to move the pointer naturally
* prevent fighting the animation

The exact value should be determined through UI testing.

It must be configurable internally rather than hard-coded throughout the codebase.

---

# 18. Interaction Lock

Some actions temporarily prevent automatic collapse.

Collapse must be prevented while:

```text
DRAGGING
```

or:

```text
TEXT EDITING
```

or:

```text
INTERACTIVE CONTROL ACTIVE
```

Once the interaction finishes, normal collapse behavior resumes.

---

# 19. Dragging

Dragging is a first-class interaction.

The user should be able to grab the note and move it.

```text
Mouse down
    ↓
Determine draggable region
    ↓
DRAGGING
    ↓
Mouse movement
    ↓
Move note
    ↓
Mouse release
```

---

# 20. Draggable Region

The initial draggable region should be the note header.

Example:

```text
┌──────────────────────────────┐
│ ████████████████████████████ │ ← drag
├──────────────────────────────┤
│ content                      │
│                              │
└──────────────────────────────┘
```

The content editor should not interpret normal text selection as a drag.

Controls should remain clickable.

---

# 21. Drag Position

During dragging:

```text
NoteWindow
    ↓
mouse delta
    ↓
new geometry
```

The note should follow the pointer naturally.

The pointer's original offset within the header should be preserved.

This prevents the note from jumping when dragging begins.

---

# 22. Dock Detection

When dragging finishes, Comma determines whether the note is close enough to an edge to dock.

Conceptually:

```text
                     screen
┌───────────────────────────────────────┐
│                                       │
│                   ┌──────────────┐    │
│                   │     NOTE     │    │
│                   └──────────────┘    │
│                                       │
└───────────────────────────────────────┘
                         ↓
                    drag right
                         ↓
┌───────────────────────────────────────┐
│                                 ┌─────┤
│                                 │NOTE │
└─────────────────────────────────┴─────┘
                         ↓
                       SNAP
```

If the note enters the configured docking threshold:

```text
free position
    ↓
edge threshold
    ↓
dock
```

Otherwise, the note remains at its free position.

---

# 23. Dock Snap

Docking should have a subtle snap animation.

The note should not teleport.

```text
User releases
      ↓
Detect edge
      ↓
Calculate final dock position
      ↓
Animate
      ↓
DOCKED
```

The final position becomes the persisted position/state.

---

# 24. Rearranging Notes

The reference explicitly demonstrates rearranging notes.

For the right-side dock, notes are arranged vertically.

Example:

```text
RIGHT EDGE

┌──────┐
│  A   │
├──────┤
│  B   │
├──────┤
│  C   │
└──────┘
```

The user may change their order.

After rearrangement:

```text
┌──────┐
│  C   │
├──────┤
│  A   │
├──────┤
│  B   │
└──────┘
```

---

# 25. Rearrangement Model

Each docked note should have an ordering value.

For example:

```text
order = 0
order = 1
order = 2
```

The exact implementation may use list ordering instead.

The important rule is:

> Dock order must be deterministic and persistent.

---

# 26. Rearranging by Drag

The preferred interaction is:

```text
Grab note
   ↓
Drag
   ↓
Move toward desired location
   ↓
Other notes make room
   ↓
Release
   ↓
New order
```

This should feel like physically rearranging a stack rather than manually editing numeric positions.

---

# 27. Expanded Note and Other Notes

When one note expands:

```text
Note A → EXPANDED
```

other notes should remain available.

They must not unexpectedly disappear.

Possible behavior:

```text
A expanded

                ┌──────────────┐
                │      A       │
                │              │
                └──────────────┘

                          ┌─────┐
                          │ B   │
                          ├─────┤
                          │ C   │
                          └─────┘
```

The expanded note should not permanently rearrange unrelated notes.

---

# 28. Overlap

Expanded notes may temporarily occupy the same desktop region.

However, Comma should avoid intentionally creating severe overlap when arranging docked notes.

The user remains in control of free-form note placement.

Automatic collision management should be conservative.

Comma should not constantly move a user's notes around.

---

# 29. Multiple Expanded Notes

The architecture should allow multiple notes to be expanded simultaneously.

However, the initial interaction may choose to prioritize one active expanded note.

This behavior should remain configurable at the interaction layer.

The default implementation should favor:

> predictable interaction over maximum simultaneous expansion.

---

# 30. Note Colors

Each note may have a color.

Color is persistent.

Changing color:

```text
User selects color
       ↓
Note appearance changes
       ↓
Model updates
       ↓
Persistence
```

Color selection must not create a new note.

---

# 31. Archive

Archive is a secondary lifecycle action.

User:

```text
Archive
   ↓
Note closes
   ↓
Removed from active desktop
   ↓
Stored as archived
```

The note must remain recoverable.

Archive is not delete.

---

# 32. Export

Export should be available from the note's secondary controls.

Example:

```text
Export
  ↓
Choose destination
  ↓
Serialize note
  ↓
Write file
  ↓
Keep original note unchanged
```

Exporting must not archive or delete the note.

---

# 33. Delete

Delete is destructive.

The user should be clearly distinguished between:

```text
Archive
```

and:

```text
Delete
```

Recommended hierarchy:

```text
Primary:
Note content

Secondary:
Archive / Export

Danger:
Delete
```

---

# 34. Creating a Note

The user must have a simple way to create a new note.

The initial creation flow should be:

```text
New Note
   ↓
Create Note model
   ↓
Create NoteWindow
   ↓
Show expanded
   ↓
Focus editor
```

A new note should be immediately usable.

The exact creation shortcut/UI entry point will be finalized separately.

---

# 35. Closing a Note

Closing a note window must not mean deleting it.

Depending on the final UI:

```text
Close / dismiss
      ↓
Return to dock
```

or:

```text
Close application
      ↓
Persist workspace
```

The semantic distinction must remain:

```text
Window lifecycle ≠ Note lifecycle
```

---

# 36. Window Lifecycle

A note window can be:

```text
created
shown
expanded
collapsed
hidden
destroyed
recreated
```

The underlying note can remain:

```text
active
```

throughout those transitions.

---

# 37. Application Restart

After restart:

```text
Comma starts
    ↓
Load workspace
    ↓
Restore active notes
    ↓
Restore their order
    ↓
Restore colors
    ↓
Restore content
    ↓
Restore dock positions
```

The user should see essentially the same workspace they left.

---

# 38. Accidental Interaction Prevention

Comma must avoid:

* accidental note movement
* accidental deletion
* accidental collapse
* accidental archive
* accidental text loss

Interactions with destructive consequences should require intentional input.

---

# 39. Accessibility / Usability

The note should remain usable without relying exclusively on color.

Color is an identity cue, not the only indicator.

Text and controls should maintain readable contrast.

Keyboard navigation should be considered during implementation.

---

# 40. Interaction State Machine

The complete initial state machine:

```text
                       ┌────────────┐
                       │   DOCKED   │
                       └─────┬──────┘
                             │
                           hover
                             │
                             ▼
                       ┌────────────┐
                       │ EXPANDING  │
                       └─────┬──────┘
                             │
                             ▼
                       ┌────────────┐
                       │  EXPANDED  │
                       └──┬─────┬───┘
                          │     │
                       drag    leave
                          │     │
                          ▼     ▼
                    ┌────────┐ ┌────────────┐
                    │ DRAGGING│ │ COLLAPSING │
                    └────┬───┘ └──────┬─────┘
                         │             │
                      release          │
                         │             │
                         ▼             ▼
                    ┌─────────┐   ┌─────────┐
                    │ DOCKING │──►│ DOCKED  │
                    └─────────┘   └─────────┘
```

---

# 41. Event Rules

| Event                      | Expected behavior          |
| -------------------------- | -------------------------- |
| Hover docked tab           | Begin expansion            |
| Click docked tab           | Expand / activate          |
| Mouse enters expanded note | Remain expanded            |
| Mouse leaves expanded note | Begin collapse timer       |
| Start editing              | Prevent collapse           |
| Start dragging             | Enter dragging state       |
| Move during drag           | Update geometry            |
| Release near edge          | Snap/dock                  |
| Release away from edge     | Keep free position         |
| Archive                    | Remove from active desktop |
| Export                     | Write copy, keep note      |
| Delete                     | Permanently remove         |
| Create                     | Show new expanded note     |
| Application restart        | Restore workspace          |

---

# 42. Timing Rules

Timing values should be centralized.

Conceptually:

```python
INTERACTION = {
    "expand_duration": ...,
    "collapse_duration": ...,
    "collapse_delay": ...,
    "dock_duration": ...,
}
```

No timing values should be scattered across multiple widgets.

This makes visual tuning possible without architectural changes.

---

# 43. Interaction Priorities

When interactions conflict, Comma follows this priority:

```text
1. Active user input
2. Dragging
3. Text editing
4. Explicit control interaction
5. Hover behavior
6. Automatic collapse
```

Therefore:

> Automatic behavior must never interrupt explicit user interaction.

---

# 44. Reference Fidelity

The implementation should reproduce the **behavioral character** of the reference rather than blindly copying implementation details.

Required:

* Edge-resident notes
* Partial docked visibility
* Hover reveal
* Inward expansion
* Direct editing
* Multiple colored notes
* Rearrangement
* Archive/export actions

Not required:

* Exact pixel-for-pixel reproduction
* Exact fonts
* Exact colors
* Exact animation duration
* Exact Mac-only window implementation

---

# 45. Open Decisions

The following are intentionally unresolved and must be decided before their respective implementation phases:

### O1

Exact docked tab width.

### O2

Exact expanded note dimensions.

### O3

Expand animation duration.

### O4

Collapse delay.

### O5

Whether click should expand when hover already exists.

### O6

Whether multiple notes may remain expanded simultaneously.

### O7

Exact drag/rearrangement gesture.

### O8

Exact edge snap threshold.

### O9

Default note color sequence.

### O10

New-note creation mechanism.

### O11

Keyboard shortcut set.

These should not be randomly decided inside implementation code.

---

# 46. Interaction Definition of Done

The interaction system is considered complete when:

* A note can remain docked on the screen edge.
* The docked note is partially visible.
* Hover reveals the note.
* Expansion is animated.
* The note can be edited directly.
* The note does not collapse during active interaction.
* The note can be dragged.
* Dragging preserves pointer offset.
* Notes can be rearranged.
* Notes can snap to the dock.
* Multiple notes can coexist.
* Archive and export actions work.
* Interaction state transitions are deterministic.
* Workspace state survives application restart.

---

# 47. Golden Rule

The single most important interaction rule is:

> **Comma should react to the user's intent, not fight it.**

If the user is reading, let them read.

If they are typing, let them type.

If they are dragging, let them drag.

If they stop interacting, Comma quietly gets out of the way.
