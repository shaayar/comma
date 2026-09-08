# Phase 3: Hover Reveal & Collapse

**Project:** Comma V2
**Phase:** 3
**Status:** Planned
**Primary Goal:** Introduce the hover-driven reveal and collapse interaction for docked notes.

---

# 1. Phase Objective

Phase 2 gave Comma the ability to dock notes to the desktop edge.

Phase 3 makes those docked notes usable without requiring a permanent full-size window.

The core interaction becomes:

```text id="x7b2cq"
              Docked
                 │
              hover
                 ↓
             Revealing
                 ↓
             Expanded
                 │
             mouse leave
                 ↓
             Collapsing
                 ↓
              Docked
```

The intended experience is:

> **The note is always there, but mostly invisible until the user asks for it.**

This is the interaction that transforms Comma from a conventional sticky-note application into a desktop-native note surface.

---

# 2. Target Behavior

A docked note should initially look approximately like:

```text id="8gqv5w"
┌───────────────────────────────────────────────┐
│                                               │
│                                               │
│                                      ┌────────┤
│                                      │   ●    │
│                                      │        │
└──────────────────────────────────────┴────────┘
```

When the pointer enters its visible dock region:

```text id="6h2c0e"
┌───────────────────────────────────────────────┐
│                                               │
│                         ┌─────────────────────┤
│                         │                     │
│                         │       My Note       │
│                         │                     │
│                         │   Remember this...  │
│                         │                     │
└─────────────────────────┴─────────────────────┘
```

When the user leaves the expanded note:

```text id="2v6bq0"
Expanded
   ↓
short delay
   ↓
collapse
   ↓
Docked
```

---

# 3. Scope

Phase 3 introduces:

* docked hover detection
* reveal behavior
* collapse behavior
* reveal/collapse animation
* interaction state management
* mouse-enter handling
* mouse-leave handling
* collapse delay
* protection against unwanted collapse while interacting
* smooth transitions between docked and expanded states

---

# 4. State Machine

The note window should now have explicit interaction states.

```text id="z1f7kf"
                ┌─────────────┐
                │   DOCKED    │
                └──────┬──────┘
                       │
                    hover
                       │
                       ▼
                ┌─────────────┐
                │  REVEALING  │
                └──────┬──────┘
                       │
                  animation done
                       │
                       ▼
                ┌─────────────┐
                │  EXPANDED   │
                └──────┬──────┘
                       │
                   mouse leave
                       │
                       ▼
                ┌─────────────┐
                │ COLLAPSING  │
                └──────┬──────┘
                       │
                  animation done
                       │
                       ▼
                ┌─────────────┐
                │   DOCKED    │
                └─────────────┘
```

The state should be represented explicitly rather than inferred from arbitrary window coordinates.

---

# 5. Reveal Trigger

The primary reveal trigger is:

> **Pointer enters the visible portion of a docked note.**

Conceptually:

```text id="4t7rjj"
┌───────────────────────────────────────────────┐
│                                               │
│                                      ████████ │ ← hover
└──────────────────────────────────────████████─┘
                                       ↑
                                  reveal starts
```

The note should not require a click to reveal.

This is important to the reference interaction.

---

# 6. Reveal Direction

For the initial right-edge implementation:

```text id="g0l7fz"
RIGHT EDGE

████████████████████████████████████████
                              ← reveal
```

The note expands **inward toward the desktop**.

Therefore:

```text id="39g2p7"
Docked:

                   ██████]


Expanded:

             [████████████████████]
```

The right boundary remains anchored to the screen edge.

The left boundary moves inward.

---

# 7. Animation

Unlike Phase 2, movement is now animated.

The transition should feel deliberate and lightweight.

Conceptually:

```text id="2x4f5j"
Docked
  │
  ├── frame 1
  ├── frame 2
  ├── frame 3
  ├── frame 4
  └── Expanded
```

Use Qt's animation facilities rather than implementing manual frame loops.

The exact:

* duration
* easing curve
* animation timing

are intentionally tunable.

They should be centralized configuration values.

---

# 8. Collapse Animation

When the pointer leaves the expanded note:

```text id="h3j4jp"
Expanded
    ↓
wait briefly
    ↓
collapse animation
    ↓
Docked
```

The note should return toward the right edge.

The animation should reverse the reveal movement rather than teleporting the window.

---

# 9. Collapse Delay

The note should **not immediately collapse** when the pointer briefly leaves its boundary.

A small delay should exist.

Example:

```text id="o4w2yq"
mouse leaves
     ↓
collapse timer
     ↓
if pointer returns
     ↓
cancel collapse
```

This prevents accidental flickering.

The exact delay is not finalized in Phase 3.

It should be configurable.

---

# 10. Re-Entry During Collapse

If the user moves the pointer back onto the note while it is collapsing:

```text id="7j2d7q"
COLLAPSING
     │
 pointer returns
     ↓
cancel collapse
     ↓
REVEALING / EXPANDED
```

The system must not finish collapsing first and then reveal again.

The animation should respond to the new user intent.

---

# 11. Editing Protection

A major requirement:

> **A note must never collapse while the user is actively interacting with it.**

For example:

```text id="9c8tqj"
User:
hover → reveal → click → type
```

The note must remain expanded while the user is typing.

The collapse mechanism must recognize:

* text focus
* active text editing
* mouse interaction
* interaction with note controls

as reasons to delay collapse.

---

# 12. Interaction Priority

The following priority should be respected:

```text id="6ddw4e"
Active user input
       ↓
Dragging
       ↓
Text editing
       ↓
Explicit controls
       ↓
Hover
       ↓
Automatic collapse
```

Automatic collapse is the least important behavior.

If the user is doing something intentional, the automatic system must yield.

---

# 13. Focus Behavior

When a docked note is revealed:

* it should become usable
* the user should be able to interact with it immediately
* clicking inside the editor should focus the editor
* other notes must remain available

Focus should not cause unrelated notes to disappear.

Phase 3 does not define a complex focus-management system.

---

# 14. Hover Region

The visible docked region should be sufficient to discover and trigger the note.

For example:

```text id="j8d8kx"
┌───────────────────────────────────────────────┐
│                                      ┌───────┐│
│                                      │       ││
│                                      │ HOVER ││
│                                      │ AREA  ││
└──────────────────────────────────────┴───────┘
```

The hover region should correspond to the visible dock area.

Do not introduce invisible giant hover zones across the desktop.

The user should be able to understand why a note revealed itself.

---

# 15. Mouse Transition Problem

A special case occurs when the note begins revealing while the pointer is near the edge.

The implementation must avoid this sequence:

```text id="z9j6pu"
hover
  ↓
note moves inward
  ↓
pointer is no longer considered inside
  ↓
collapse
  ↓
reveal
  ↓
collapse
```

This would create flickering.

The hover/interation system must account for the moving window.

---

# 16. Animation Ownership

Animation should belong to the presentation/interaction layer.

It should not be stored inside the domain `Note`.

Correct:

```text id="n7v9m1"
Note
  ↓
NoteWindow
  ↓
Animation
```

Incorrect:

```text id="0bd2xj"
Note
  ↓
animation_progress = 0.63
```

Animation progress is runtime UI state.

It must not become part of persistent note data.

---

# 17. Persistence

Phase 3 does not introduce complete persistence.

The following runtime properties should **not** be saved continuously:

* animation progress
* hover state
* collapse timer
* reveal progress
* mouse position
* focus state

The persistent model should continue representing stable workspace state only.

---

# 18. Failure Conditions

The implementation should specifically guard against:

### Flickering

```text id="3m4b8g"
reveal → collapse → reveal → collapse
```

### Collapse while typing

The note must remain open.

### Collapse while interacting with controls

The note must remain open.

### Duplicate animations

Starting a second reveal animation should not leave the first animation fighting it.

### Stale timers

An old collapse timer must not collapse a note after the user has already returned.

### Lost note state

Animation must never overwrite or replace note content.

---

# 19. What Phase 3 Does NOT Do

## Dragging

Not yet.

The user cannot rearrange notes by dragging.

---

## Snapping

Not yet.

No automatic snap-to-edge after dragging.

---

## Multi-note Dock Arrangement

Not yet.

The final vertical stack behavior remains a later phase.

---

## Archive

Not yet.

---

## Export

Not yet.

---

## Advanced Visual Polish

No final shadows, gradients, typography systems, micro-interactions, or extensive visual tuning yet.

The animation should work first.

Polish comes later.

---

# 20. Temporary Development Controls

Temporary controls may exist to test:

```text id="p8t3w1"
Dock
Reveal
Collapse
```

These are testing mechanisms only.

The final interaction should primarily use:

```text id="q2u4l0"
Hover → Reveal
Mouse Leave → Collapse
```

---

# 21. Testing

## Test 1: Hover Reveal

1. Dock a note.
2. Move the pointer onto its visible tab.
3. Observe the note.

Expected:

```text id="8g51kg"
Docked
   ↓
Smooth reveal
   ↓
Expanded
```

---

## Test 2: Mouse Leave

1. Reveal a note.
2. Move the pointer away.
3. Wait for the collapse delay.

Expected:

```text id="3t1q7e"
Expanded
   ↓
delay
   ↓
Smooth collapse
   ↓
Docked
```

---

## Test 3: Re-entry

1. Reveal a note.
2. Move away.
3. Before collapse finishes, move back.

Expected:

* collapse is cancelled
* note remains/re-enters expanded state
* no visible flicker

---

## Test 4: Typing

1. Reveal note.
2. Click editor.
3. Type continuously.

Expected:

* note does not collapse
* content updates correctly

---

## Test 5: Moving Pointer Through Boundary

Move the pointer across the note while it is revealing.

Expected:

* no reveal/collapse loop
* no flickering
* animation remains stable

---

## Test 6: Multiple Notes

Create multiple docked notes.

Reveal one.

Expected:

* selected note reveals correctly
* other notes remain stable
* no unrelated note animation starts

---

## Test 7: Content Integrity

Reveal and collapse a note repeatedly.

Expected:

```text id="x5j5h8"
content_before == content_after
```

---

# 22. Acceptance Criteria

Phase 3 is complete when:

* [ ] Docked notes respond to hover.
* [ ] Hovering the visible dock region reveals the note.
* [ ] Right-edge notes reveal inward.
* [ ] Reveal movement is animated.
* [ ] Mouse leave initiates collapse.
* [ ] Collapse has a configurable delay.
* [ ] Collapse is animated.
* [ ] Returning to the note cancels pending collapse.
* [ ] Notes do not collapse while actively being edited.
* [ ] Notes do not collapse during explicit control interaction.
* [ ] Animation state remains runtime-only.
* [ ] No animation flickering occurs during normal interaction.
* [ ] Multiple docked notes remain independent.
* [ ] Note content survives repeated reveal/collapse cycles.
* [ ] No dragging/rearrangement has been introduced.
* [ ] No archive/export system has been introduced.
* [ ] Tests pass.

---

# 23. Phase 3 Definition of Done

The fundamental interaction should now feel like:

```text id="a7m8n2"
             ┌───────────────┐
             │               │
             │     NOTE      │
             │               │
             └───────────────┘
                    ▲
                    │
                  hover
                    │
                    ▼
              ┌──────────┐
              │   TAB    │
              └──────────┘
                    │
                 collapse
                    │
                    ▼
                 desktop
                   edge
```

The user should be able to glance at the desktop, encounter a small note tab, hover it, use the note, and leave it behind without manually opening or closing an application.

The architectural result is:

> **Docking is now an interaction, not merely a coordinate.**

---

# 24. Phase Gate

Do not begin Phase 4 until Phase 3 reliably passes its acceptance criteria.

The next phase will introduce:

> **Dragging, edge snapping, and intentional repositioning of notes.**

That phase will make the desktop note surface physically rearrangeable.
