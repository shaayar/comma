# Phase 8: Visual Polish & Reference-Level Experience

**Project:** Comma V2
**Phase:** 8
**Status:** Planned
**Primary Goal:** Transform the functional V2 foundation into a cohesive, polished desktop note experience closely aligned with the reference interaction and Comma's visual identity.

---

# 1. Phase Objective

Phases 1 through 7 established Comma's functional system:

```text
Independent Notes
       ↓
Desktop Windows
       ↓
Edge Docking
       ↓
Hover Reveal
       ↓
Dragging
       ↓
Multi-Note Dock
       ↓
Persistence
       ↓
Archive / Export
```

Phase 8 does not fundamentally change that architecture.

Instead, it answers:

> **What should Comma actually feel like to use?**

The goal is to eliminate the appearance of a prototype and create a deliberate, lightweight desktop experience.

---

# 2. Design Direction

The reference establishes a clear visual philosophy:

```text
minimal
    +
quiet
    +
colorful
    +
desktop-native
    +
interaction-driven
```

Comma should feel present without constantly demanding attention.

The desktop should remain visually dominant.

The notes should feel like objects belonging to the desktop rather than panels from a conventional productivity application.

---

# 3. Core Visual Principle

The visual hierarchy should be:

```text
Desktop
   ↓
Small dock presence
   ↓
Reveal
   ↓
Focused note
```

A docked note should be visually quiet.

An expanded note should become visually clear and readable.

The transition between these states is part of the product identity.

---

# 4. Note Appearance

The final note should have a compact, recognizable structure.

Conceptually:

```text
┌───────────────────────────────┐
│ ●  My Note              ⋯     │
├───────────────────────────────┤
│                               │
│ Remember to call Alice        │
│ about the project.            │
│                               │
│                               │
├───────────────────────────────┤
│        archive   export       │
└───────────────────────────────┘
```

The exact layout may evolve.

The visual hierarchy should remain:

```text
Header
  ↓
Content
  ↓
Secondary controls
```

---

# 5. Color System

Notes should use a small, intentional color palette.

The palette should provide enough variation for users to distinguish notes without turning Comma into a rainbow control panel.

Possible conceptual palette:

```text
Yellow
Blue
Green
Pink
Purple
Orange
```

The exact final colors should be chosen during implementation based on:

* readability
* contrast
* visual harmony
* light/dark desktop environments

---

# 6. Color Meaning

Color should remain primarily visual.

It must not encode hidden semantics such as:

```text
red = urgent
green = completed
blue = work
```

unless explicitly introduced as a future feature.

A user changing a note's color should not accidentally change its meaning or behavior.

---

# 7. Contrast

Text must remain readable against every supported note color.

For each color:

```text
background
    ↓
calculate/select readable foreground
```

Do not choose colors solely because they look attractive in isolation.

The note must remain usable.

---

# 8. Typography

Typography should be:

* clean
* compact
* readable
* consistent

The title should have clear hierarchy over the content.

For example:

```text
TITLE
────────────────
Body text begins here...
```

Avoid excessive typography.

No:

* decorative fonts
* excessive font weights
* unnecessary capitalization
* giant headings

Comma is a desktop tool, not a magazine cover.

---

# 9. Content Area

The editor should remain the visual center of the expanded note.

It should feel like:

```text
┌───────────────────────┐
│ Title                 │
├───────────────────────┤
│                       │
│ Type here...          │
│                       │
│                       │
└───────────────────────┘
```

Avoid excessive borders or UI chrome.

The editor should visually blend into the note.

---

# 10. Header

The header should communicate:

* note identity
* draggable region
* available controls

without becoming visually heavy.

The draggable area should be large enough to comfortably grab.

The header should also remain clearly distinct from the editable content area.

---

# 11. Controls

Controls should remain minimal.

Potential controls include:

```text
Archive
Export
Color
```

Controls should not permanently dominate the note.

They may use:

* subtle icons
* compact buttons
* hover states
* low visual weight

The final control arrangement should be determined during implementation.

---

# 12. Control Visibility

The reference experience favors a quiet interface.

Therefore secondary controls may be:

```text
visible on hover
```

or otherwise visually subdued.

However:

> **Important actions must remain discoverable.**

Do not hide everything behind an unexplained gesture.

---

# 13. Note Corners

The note shape should feel soft and lightweight.

Potential treatment:

```text
rounded corners
```

with a restrained radius.

Avoid exaggerated card styling.

Comma should still feel like a desktop note rather than a web dashboard card.

---

# 14. Shadows

Expanded notes should visually separate from the desktop.

A restrained shadow can communicate:

```text
desktop
   ↓
floating note
```

The shadow should be:

* subtle
* soft
* consistent

Avoid large decorative shadows.

---

# 15. Docked Appearance

When docked, the note should expose only enough visual information to communicate:

> "There is a note here."

The dock should not dominate the desktop.

Possible visible elements:

```text
┌──────┐
│  ●   │
│      │
└──────┘
```

or a narrow colored strip/tab.

The exact dock-tab design should be finalized through visual testing.

---

# 16. Dock Tab Identity

Multiple notes must remain distinguishable when docked.

The user should be able to tell:

```text
Note A
Note B
Note C
```

apart without expanding every note.

Possible identity signals:

* color
* title fragment
* small indicator
* consistent tab structure

The implementation should prefer the simplest effective signal.

---

# 17. Hover States

Hover should provide subtle feedback.

Examples:

```text
normal
  ↓
slightly emphasized
```

Controls may become more visible on hover.

Do not make hover states excessively animated.

Hover feedback should communicate interaction readiness rather than become decoration.

---

# 18. Reveal Animation Refinement

Phase 3 established functional reveal animation.

Phase 8 tunes it.

The desired sequence:

```text
hover
  ↓
quick response
  ↓
smooth reveal
  ↓
settle
```

It should not feel:

* sluggish
* mechanical
* abrupt
* bouncy without reason

The exact duration and easing should be selected through repeated real-world interaction testing.

---

# 19. Collapse Animation Refinement

Collapse should feel like the inverse of reveal:

```text
Expanded
   ↓
brief delay
   ↓
smooth retreat
   ↓
Docked
```

The collapse should never feel like Comma is forcibly removing the note.

It should feel like the note is returning to its resting state.

---

# 20. Animation Consistency

Reveal, collapse, and docking animations should use a coherent motion language.

Avoid:

```text
reveal = one style
collapse = completely different style
snap = unrelated style
```

Instead:

```text
Comma Motion System
       │
       ├── Reveal
       ├── Collapse
       └── Snap
```

with shared timing/easing principles.

---

# 21. Drag Visual Feedback

While dragging:

* note should remain clearly visible
* note should appear active
* dock behavior should remain understandable
* pointer interaction should feel direct

A subtle visual elevation may be used.

For example:

```text
Normal
  ↓
Dragging
  ↓
slightly stronger shadow
```

Do not make the note visually transform into an entirely different component.

---

# 22. Dock Rearrangement Feedback

During vertical rearrangement, the user should understand where the note will land.

A possible interaction:

```text
Note A
────────────
Note B
────────────
      ↑
   insertion
    point
────────────
Note C
```

The feedback should remain subtle.

The goal is clarity, not visual spectacle.

---

# 23. Focus State

The currently active note should be visually distinguishable without becoming loud.

Possible cues:

* slightly stronger shadow
* subtle border
* stronger header contrast

Avoid:

* large outlines
* flashing
* dramatic color changes

---

# 24. Empty Note State

A newly created note should make it obvious where to type.

For example:

```text
┌────────────────────────┐
│ Untitled               │
├────────────────────────┤
│                        │
│ Start typing...        │
│                        │
└────────────────────────┘
```

The placeholder should disappear naturally once content is entered.

---

# 25. New Note Experience

Creating a note should feel immediate.

The intended sequence:

```text
Create
  ↓
Note appears
  ↓
Note is focused
  ↓
Cursor ready
  ↓
Type
```

Avoid forcing the user through:

```text
Create
 ↓
dialog
 ↓
enter title
 ↓
choose color
 ↓
confirm
 ↓
open note
```

unless a future requirement explicitly demands it.

---

# 26. Archive Experience

Archiving should feel deliberate but lightweight.

A good interaction:

```text
Archive
   ↓
note leaves desktop
   ↓
dock reflows
```

Avoid unnecessary confirmation dialogs for ordinary archive actions.

Archive is reversible.

---

# 27. Export Experience

Export should use the operating system's normal save interaction.

The UI should not create a custom complex file browser.

The experience should be:

```text
Export
  ↓
Save dialog
  ↓
Choose location
  ↓
Done
```

---

# 28. Archived Notes Visual Design

The archive view should use the same visual language as the notes.

It should not suddenly look like:

```text
corporate database software
```

Keep it:

* compact
* readable
* simple
* consistent with Comma

---

# 29. Empty Archive

If there are no archived notes:

```text
Archived Notes

No archived notes yet.
```

The empty state should explain what the user can expect without unnecessary decoration.

---

# 30. Window Chrome

The final V2 note windows should avoid unnecessary operating-system chrome if the reference experience calls for a frameless design.

However, native behavior must not be sacrificed merely for appearance.

The implementation should preserve:

* focus behavior
* accessibility where practical
* predictable window management
* correct positioning

---

# 31. Desktop Presence

Comma should remain visually lightweight even when many notes exist.

The application should avoid:

* permanent central dashboards
* large navigation panels
* persistent toolbars
* unnecessary status bars

The desktop itself is the workspace.

---

# 32. Application Identity

Comma's visual identity should emerge from:

```text
small notes
+
color
+
motion
+
edge presence
+
minimal controls
```

rather than from a large logo or branding panel.

The application name does not need to occupy the desktop constantly.

---

# 33. Theme Support

If theme support already exists, Phase 8 should refine it.

At minimum:

```text
Light
Dark
```

should remain coherent.

The note colors must remain readable in both environments.

Do not create a separate visual system for every possible theme.

---

# 34. Accessibility

Visual polish must not reduce usability.

Check:

* text contrast
* clickable control size
* keyboard focus
* editor readability
* hover-only information
* color-only distinctions

Color must not be the only way to distinguish important states.

---

# 35. Keyboard Interaction

Phase 8 should ensure that existing keyboard interaction remains usable.

At minimum:

* text editing works naturally
* standard text shortcuts work
* focus can move predictably
* controls can be reached where practical

A desktop note should not become mouse-only simply because it looks cleaner.

---

# 36. Performance

Visual polish must not introduce noticeable performance degradation.

Particularly check:

* multiple note windows
* simultaneous animations
* repeated hover transitions
* dock rearrangement
* autosave
* large numbers of notes

The UI should remain responsive.

---

# 37. Number of Notes

Phase 8 should test realistic workloads.

At minimum test:

```text
1 note
5 notes
10 notes
20 notes
```

The exact supported maximum is not defined here.

The objective is to identify obvious performance or layout failures before release.

---

# 38. Reference Comparison

The final implementation should be compared against the reference experience for:

### Presence

Do notes feel like edge-mounted desktop objects?

### Reveal

Does hovering reveal naturally?

### Motion

Does the movement feel smooth?

### Density

Are multiple notes visually manageable?

### Interaction

Can the user understand how to reveal and move notes without instructions?

### Restraint

Does the application stay visually quiet when not being used?

---

# 39. Visual Consistency Rules

The following should remain consistent:

```text
Corner radius
Spacing
Typography
Control sizing
Animation timing
Dock width
Shadow treatment
Color palette
```

These values should be centralized where practical.

Avoid scattering magic numbers throughout the codebase.

---

# 40. What Phase 8 Does NOT Do

Phase 8 is a polish phase.

Do not introduce unrelated product features.

Do not add:

* AI assistance
* synchronization
* accounts
* collaboration
* reminders
* calendar integration
* mobile clients
* browser extensions
* plugins
* advanced search
* tagging systems

A visual-polish phase must remain a visual-polish phase.

---

# 41. Testing

## Test 1: Visual Hierarchy

Open one note.

Expected:

* title is clearly identifiable
* content is easiest to read
* controls are secondary

---

## Test 2: Docked Appearance

Dock multiple notes.

Expected:

* desktop remains visually clean
* notes remain distinguishable
* dock does not dominate the screen

---

## Test 3: Hover Reveal

Hover a docked note.

Expected:

* reveal starts quickly
* animation is smooth
* final position feels stable

---

## Test 4: Collapse

Leave the note.

Expected:

* brief delay
* smooth collapse
* no sudden teleportation

---

## Test 5: Rapid Hover

Repeatedly enter and leave the dock region.

Expected:

* no flicker
* no animation conflicts
* no stuck states

---

## Test 6: Drag

Drag an expanded note.

Expected:

* movement remains direct
* note remains visually readable
* controls do not interfere

---

## Test 7: Rearrangement

Rearrange several notes.

Expected:

* insertion position is understandable
* final stack is visually clean
* no overlap occurs

---

## Test 8: Theme

Test supported themes.

Expected:

* readable text
* consistent controls
* note colors remain usable

---

## Test 9: Large Note Count

Test:

```text
1
5
10
20
```

notes.

Expected:

* application remains responsive
* dock remains understandable
* no major rendering degradation

---

## Test 10: Restart

Restart with a populated workspace.

Expected:

* polished appearance remains consistent
* restored notes retain expected geometry
* dock arrangement remains correct

---

# 42. Acceptance Criteria

Phase 8 is complete when:

* [ ] Final note visual hierarchy is established.
* [ ] Note colors form a coherent palette.
* [ ] Text remains readable across all note colors.
* [ ] Typography is consistent.
* [ ] Header and content areas are clearly differentiated.
* [ ] Controls are visually lightweight.
* [ ] Docked notes have a compact, recognizable appearance.
* [ ] Multiple docked notes remain distinguishable.
* [ ] Hover feedback is subtle and consistent.
* [ ] Reveal animation feels responsive and polished.
* [ ] Collapse animation feels natural.
* [ ] Dragging has appropriate visual feedback.
* [ ] Rearrangement provides clear insertion feedback.
* [ ] Focus state is understandable.
* [ ] Archive UI matches the Comma visual language.
* [ ] Export interaction remains simple.
* [ ] Light/dark presentation is coherent if both are supported.
* [ ] Keyboard interaction remains usable.
* [ ] Accessibility issues caused by visual styling are addressed.
* [ ] Performance remains acceptable with multiple notes.
* [ ] No unrelated product features have been introduced.
* [ ] Reference comparison has been performed.
* [ ] No major visual or interaction inconsistencies remain.

---

# 43. Phase 8 Definition of Done

Comma should now present the complete experience:

```text
                     DESKTOP
┌────────────────────────────────────────────────────┐
│                                                    │
│                                                    │
│                                                    │
│                                                    │
│                                        ┌──────────┐│
│                                        │  ● Note  ││
│                                        ├──────────┤│
│                                        │  ● Note  ││
│                                        ├──────────┤│
│                                        │  ● Note  ││
│                                        └──────────┘│
└────────────────────────────────────────────────────┘
```

Hover:

```text
                     DESKTOP
┌────────────────────────────────────────────────────┐
│                                                    │
│                              ┌─────────────────────┤
│                              │ My Note             │
│                              │                     │
│                              │ Remember this...    │
│                              │                     │
│                              │         Archive     │
│                              └─────────────────────┘
└────────────────────────────────────────────────────┘
```

Drag:

```text
                     DESKTOP
┌────────────────────────────────────────────────────┐
│                       ┌────────────────────────────┐│
│                       │ My Note                    ││
│                       │                            ││
│                       └────────────────────────────┘│
│                                                    │
└────────────────────────────────────────────────────┘
```

Return to edge:

```text
┌────────────────────────────────────────────────────┐
│                                      ┌─────────────┤
│                                      │ ● My Note   │
└──────────────────────────────────────┴─────────────┘
```

The application should now feel like **Comma**, rather than a collection of implemented features.

---

# 44. Architectural Result

Phase 8 should not significantly alter the underlying architecture.

Instead, it validates that the architecture is capable of supporting a polished experience without hacks.

The intended structure remains:

```text
AppController
      │
      ▼
 NoteManager
      │
 ┌────┴────┐
 ▼         ▼
Notes   DockManager
 │         │
 └────┬────┘
      ▼
 NoteWindows
      │
      ▼
Presentation
```

Visual polish belongs above the domain model, not inside it.

---

# 45. Phase Gate

Do not begin Phase 9 until Phase 8 passes its acceptance criteria.

The final phase will be:

> **Testing, packaging, release hardening, and final V2 validation.**

That phase is where we stop adding things and try very hard to break everything we have built.
