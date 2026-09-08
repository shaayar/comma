# Phase 9: Testing, Packaging & Release Hardening

**Project:** Comma V2
**Phase:** 9
**Status:** Planned
**Primary Goal:** Validate, harden, package, and prepare Comma V2 for reliable real-world use.

---

# 1. Phase Objective

All major V2 functionality should already exist.

Phase 9 is deliberately different from previous phases.

We are no longer asking:

> "What feature should we build next?"

We are asking:

> **"Can we trust what we built?"**

The application must survive:

* normal usage
* unusual interaction
* repeated interaction
* restart cycles
* corrupted data
* multiple notes
* different screen configurations
* installation
* application shutdown
* unexpected interruptions

The goal is to move from:

```text
Functional Prototype
        ↓
Reliable Application
```

---

# 2. Complete V2 Feature Set

Before entering Phase 9, Comma should contain:

```text id="1y3x8c"
Independent Notes
      ↓
Desktop Windows
      ↓
Right-Edge Docking
      ↓
Hover Reveal
      ↓
Collapse
      ↓
Dragging
      ↓
Edge Snapping
      ↓
Multi-Note Dock
      ↓
Rearrangement
      ↓
Persistence
      ↓
Archive
      ↓
Export
      ↓
Visual Polish
```

Phase 9 validates this entire chain.

---

# 3. Release Candidate Rule

No new user-facing functionality should be introduced during the final validation pass unless it fixes a release-blocking defect.

This distinction is important.

### Allowed

```text
Bug fix
Performance fix
Crash fix
Persistence repair
Accessibility fix
Packaging fix
Visual inconsistency fix
```

### Not allowed

```text
New feature
New interaction system
New settings system
New integration
New major UI concept
```

Feature ideas discovered during Phase 9 should be recorded for a future roadmap rather than immediately implemented.

---

# 4. Testing Strategy

Testing should occur at four levels:

```text id="8q4m2x"
        ┌──────────────────┐
        │ Integration Test │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │   UI Validation  │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  System Testing  │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Release Testing  │
        └──────────────────┘
```

---

# 5. Unit Testing

Existing domain and application tests should be expanded.

Test:

* `Note`
* `NoteManager`
* `DockManager`
* workspace serialization
* workspace validation
* migration
* export
* geometry calculations

Domain tests should not require an actual desktop window where unnecessary.

---

# 6. Note Model Tests

Verify:

* unique IDs
* valid defaults
* title handling
* content handling
* color handling
* geometry
* dock state
* order
* archive state

Examples:

```text id="2n8q6v"
empty note
large note
empty title
long title
large content
special characters
unicode content
```

All should behave safely.

---

# 7. NoteManager Tests

Verify:

* creation
* lookup
* modification
* removal
* archiving
* restoration
* active-note filtering
* archived-note filtering
* multiple-note isolation

Important invariant:

```text id="7x3m9p"
Removing Window
      ≠
Removing Note
```

---

# 8. DockManager Tests

Verify:

* right-edge positioning
* docking
* undocking
* ordering
* reordering
* spacing
* variable note heights
* overflow handling
* screen geometry changes

Test deterministic output.

Given:

```text id="k4r7p1"
same notes
same order
same screen geometry
```

the resulting layout should be the same.

---

# 9. Persistence Tests

Persistence should receive especially aggressive testing.

Verify:

```text id="m6q2v9"
Create
Edit
Move
Resize
Dock
Reorder
Archive
Restore
Export
Quit
Restart
```

and confirm that the expected state survives.

---

# 10. Restart Matrix

Run repeated restart cycles.

Example:

```text id="q9v4m1"
Cycle 1:
Create A/B/C

Cycle 2:
Move A

Cycle 3:
Dock B

Cycle 4:
Reorder C

Cycle 5:
Archive A

Cycle 6:
Restore A

Cycle 7:
Resize B

Cycle 8:
Restart
```

After every cycle, validate workspace integrity.

There should be no progressive corruption.

---

# 11. Persistence Integrity

After repeated changes, verify:

```text id="x8m3r5"
IDs remain stable
No duplicate notes
No missing notes
Order remains valid
Dock state remains valid
Content remains intact
Archived notes remain archived
```

---

# 12. Autosave Testing

Verify autosave under:

* normal typing
* rapid typing
* repeated edits
* title changes
* color changes
* movement
* resizing
* docking
* rearrangement

The application should not become sluggish because of excessive writes.

---

# 13. Crash-Resistance Testing

Test situations such as:

```text id="w4p8n2"
app starts
user edits
app closes unexpectedly
```

and:

```text id="g5x1r7"
save occurring
application interrupted
```

The objective is to ensure the workspace does not become unusable.

Atomic storage behavior should be verified.

---

# 14. Corrupted Data Testing

Intentionally test:

```text id="r7m3q9"
invalid JSON
missing schema version
unknown schema version
missing notes array
invalid note object
duplicate IDs
invalid coordinates
invalid dimensions
invalid edge
invalid order
invalid archive value
```

Expected:

> Comma fails gracefully and protects recoverable user data.

---

# 15. Migration Testing

If older Comma data is supported:

```text id="x2k6v8"
Old workspace
     ↓
Migration
     ↓
Current workspace
```

must be tested using representative old files.

Verify:

* content is preserved
* note identity is handled correctly
* unsupported fields do not corrupt the workspace
* migration is deterministic

---

# 16. UI Interaction Testing

Test the complete interaction chain.

## Scenario A

```text id="v8q3m1"
Create
 ↓
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

Expected:

No glitches or unexpected state changes.

---

## Scenario B

```text id="r4x9k2"
Dock
 ↓
Reveal
 ↓
Drag
 ↓
Move away
 ↓
Release
```

Expected:

Floating note remains usable.

---

## Scenario C

```text id="p7m2c5"
Dock
 ↓
Reveal
 ↓
Drag vertically
 ↓
Reorder
 ↓
Release
```

Expected:

Dock order updates correctly.

---

# 17. Hover Stress Testing

Rapidly perform:

```text id="n6x1q8"
enter
leave
enter
leave
enter
leave
```

Expected:

* no flickering
* no stuck animation
* no disappearing note
* no orphaned timers
* no unexpected collapse

---

# 18. Drag Stress Testing

Repeatedly:

```text id="c8m4v2"
grab
drag
release
```

across:

* center
* near edge
* far edge
* top
* bottom

Expected:

* no crashes
* no lost note
* no invalid coordinates
* correct docking behavior

---

# 19. Multi-Note Stress Testing

Test with approximately:

```text id="z2r7m5"
1 note
5 notes
10 notes
20 notes
```

Validate:

* responsiveness
* dock layout
* hover behavior
* dragging
* rearrangement
* persistence

The exact maximum supported number does not need to be defined unless a release requirement demands one.

---

# 20. Long Content Testing

Create notes containing:

* one line
* many lines
* very long paragraphs
* Unicode
* emojis
* symbols
* punctuation
* mixed languages
* whitespace

Example:

```text id="k9x3v7"
Hello 🌱
नमस्ते
こんにちは
Special: !@#$%^&*()
```

Expected:

* content remains readable
* content persists correctly
* export preserves the text appropriately
* UI remains stable

---

# 21. Long Title Testing

Test:

```text id="m5q8r2"
empty title
short title
normal title
very long title
special characters
Unicode title
```

The UI should prevent titles from destroying the layout.

---

# 22. Window Geometry Testing

Test:

* very small notes
* normal notes
* large notes
* resized notes
* notes near each screen edge

Verify:

* no inaccessible states
* no permanent off-screen notes
* valid dimensions after restart

---

# 23. Screen Configuration Testing

Test where practical:

```text id="w1p6n8"
different resolutions
different aspect ratios
taskbar visible
taskbar positioned differently
external monitor connected
external monitor removed
```

The key requirement is graceful recovery.

---

# 24. Application Lifecycle Testing

Test:

```text id="q3v8m1"
Launch
 ↓
Create
 ↓
Use
 ↓
Minimize/desktop switching
 ↓
Restore focus
 ↓
Quit
 ↓
Restart
```

Verify that no state is lost.

---

# 25. Focus Testing

With multiple notes:

```text id="r5x2k7"
Note A
Note B
Note C
```

switch focus repeatedly.

Expected:

* correct active window
* typing goes to intended note
* no accidental edits to another note
* hover behavior remains stable

---

# 26. Archive Testing

Test:

```text id="g8m3q1"
active → archive
archived → restore
```

repeatedly.

Expected:

* no duplicate windows
* no duplicate notes
* dock reflows correctly
* state persists

---

# 27. Export Testing

Export:

* active note
* archived note
* empty note
* long note
* Unicode note
* special-character title

Verify:

* correct file generated
* correct content
* safe filename
* no state mutation

---

# 28. Export/Archive Independence

Verify:

```text id="x7p4m2"
Export
```

does not archive.

And:

```text id="n5q8v3"
Archive
```

does not export.

These operations must remain independent.

---

# 29. Visual Regression Testing

Compare the final implementation against the approved reference behavior.

Review:

### Dock

Does it remain visually quiet?

### Reveal

Does the note emerge naturally?

### Expanded state

Does the note feel like a desktop object?

### Multiple notes

Does the edge stack remain understandable?

### Dragging

Does the note feel directly manipulable?

### Controls

Are they discoverable without becoming visual noise?

---

# 30. Platform Testing

Comma is intended to support desktop environments.

At minimum, validate the target platforms that the release intends to support.

Potential targets:

```text id="f2k7m4"
Windows
macOS
Linux
```

If a platform is not being released in V2, it should not be treated as a release blocker.

The supported-platform list must be explicitly declared before packaging.

---

# 31. Platform-Specific Behavior

Pay particular attention to:

* always-on-top behavior
* frameless windows
* screen geometry
* taskbar/system panel interaction
* window activation
* file dialogs
* application shutdown
* startup behavior

A behavior that works on one operating system must not automatically be assumed to work on another.

---

# 32. Packaging

Create a production build process.

The packaged application should:

* launch without a development environment
* contain required Python/runtime dependencies
* include required assets
* locate its workspace correctly
* handle user data directories correctly
* have a proper application name
* have application icon assets

---

# 33. Build Reproducibility

The build process should be documented.

A clean environment should be capable of producing the application using the documented process.

Avoid relying on:

```text id="y8q3m1"
developer-specific paths
local environment variables
untracked files
manual copying
```

---

# 34. User Data Location

The production application should distinguish between:

```text id="v4x7n2"
Application files
```

and:

```text id="p8m3q6"
User workspace data
```

User notes should not depend on the application's installation directory being writable.

The final storage location should follow platform-appropriate conventions.

---

# 35. Configuration

Production configuration should not require users to edit Python source code.

Development-only values such as:

```text id="q5n8m1"
debug mode
animation debugging
test storage
```

must be disabled or isolated from normal release behavior.

---

# 36. Logging

Introduce lightweight diagnostic logging where useful.

Logs should help identify:

* startup failures
* workspace load failures
* save failures
* migration failures
* export failures
* unexpected runtime errors

Logging should not expose unnecessary user note content.

---

# 37. Error Handling

The final application must not crash for ordinary user mistakes.

Examples:

```text id="k3x7p9"
cancel export
invalid save location
corrupt workspace
off-screen note
unexpected window state
```

The application should recover whenever possible.

---

# 38. Performance Validation

Measure or manually assess:

* startup time
* workspace loading
* note creation
* hover reveal
* collapse
* dragging
* rearrangement
* autosave
* restart

The application should feel lightweight.

The central performance principle remains:

> **A desktop note application should never feel heavier than the notes it manages.**

---

# 39. Resource Usage

Check for:

* orphaned windows
* orphaned timers
* animation objects that never terminate
* repeated signal connections
* unnecessary file writes
* memory growth after repeated create/delete cycles

Perform repeated cycles:

```text id="m2q8v5"
Create
 → archive
 → restore
 → delete
 → repeat
```

and inspect for obvious resource leaks.

---

# 40. Security and Privacy

Comma is a local-first application.

Verify that the release does not unexpectedly:

* upload note content
* transmit workspace data
* require network access
* embed analytics that capture note content

The V2 architecture contains no cloud synchronization requirement.

---

# 41. Clean Installation Test

Perform a clean installation on a machine/environment without the development setup.

Verify:

```text id="x6r3p9"
Install
 ↓
Launch
 ↓
Create note
 ↓
Edit
 ↓
Quit
 ↓
Restart
```

Everything should work without developer tooling.

---

# 42. Upgrade Test

If an existing Comma installation is being upgraded:

```text id="n7m4k2"
V1
 ↓
Install V2
 ↓
Launch
 ↓
Migration
```

verify that supported existing data remains recoverable.

If V1 migration is not part of the release, this must be explicitly documented rather than silently assumed.

---

# 43. Final Regression Suite

Before release, execute one complete scenario:

```text id="v3q8m1"
1. Launch Comma
2. Create Note A
3. Create Note B
4. Create Note C
5. Edit all three
6. Change colors
7. Dock all three
8. Reveal each
9. Collapse each
10. Rearrange them
11. Drag one away
12. Snap it back
13. Archive one
14. Restore it
15. Export one
16. Move one floating
17. Resize one
18. Quit
19. Restart
20. Verify everything
```

This is the final end-to-end test.

---

# 44. Release Blocking Bugs

A release blocker includes:

* data loss
* corrupted workspace
* unrecoverable notes
* application crash during normal usage
* broken startup
* broken persistence
* broken docking
* broken editing
* broken archive/restore
* broken export
* severe interaction deadlocks
* notes becoming permanently inaccessible

These must be fixed before release.

---

# 45. Non-Blocking Issues

Minor issues may be deferred if they do not materially affect usability.

Examples:

* tiny spacing inconsistencies
* minor animation tuning
* non-critical visual imperfections
* cosmetic icon alignment

These should be recorded for a future polish pass.

---

# 46. Final Documentation

Before release, update:

```text id="j4n8p2"
README
Architecture
Data Model
Interaction Specification
Phase Documentation
Installation Instructions
Build Instructions
Supported Platforms
Known Limitations
```

The documentation should describe the application that actually exists.

Do not document planned features as if they already exist.

---

# 47. README Requirements

The final README should explain:

### What Comma is

A concise description of the desktop-note concept.

### Core features

* independent notes
* edge docking
* hover reveal
* dragging
* rearrangement
* persistence
* archive
* export

### Installation

Clear setup instructions.

### Running

Clear launch instructions.

### Development

How contributors can run the project.

### Build

How to create a release build.

### Limitations

Anything intentionally unsupported in V2.

---

# 48. Final Architecture Review

Before release, verify the architecture still follows:

```text id="s8x2m5"
AppController
      │
      ▼
 NoteManager
      │
 ┌────┴─────┐
 ▼          ▼
Notes    DockManager
 │          │
 └────┬─────┘
      ▼
 NoteWindows
      │
      ├── Interaction
      ├── Presentation
      └── Animation
     
Storage
      ↑
Workspace persistence
```

Check that no accidental shortcuts have appeared.

Especially:

```text id="p5r9x1"
NoteWindow
    ✗ direct JSON access

Domain
    ✗ PyQt dependency

DockManager
    ✗ note-content ownership

Storage
    ✗ UI responsibilities
```

---

# 49. Final Acceptance Checklist

## Core Application

* [ ] Application starts reliably.
* [ ] Notes can be created.
* [ ] Notes can be edited.
* [ ] Multiple notes work independently.
* [ ] Note identity remains stable.

## Desktop Interaction

* [ ] Right-edge docking works.
* [ ] Hover reveal works.
* [ ] Collapse works.
* [ ] Dragging works.
* [ ] Edge snapping works.
* [ ] Dock rearrangement works.

## Persistence

* [ ] Workspace saves correctly.
* [ ] Workspace loads correctly.
* [ ] State survives restart.
* [ ] Corrupted data is handled safely.
* [ ] Invalid geometry is recovered.
* [ ] Migration works where supported.

## Lifecycle

* [ ] Archive works.
* [ ] Restore works.
* [ ] Delete, if implemented, is explicit.
* [ ] Export works.
* [ ] Export does not mutate note state.

## UI

* [ ] Visual hierarchy is consistent.
* [ ] Colors are readable.
* [ ] Controls are understandable.
* [ ] Animations are stable.
* [ ] Multiple notes remain visually manageable.
* [ ] Reference interaction has been reviewed.

## Reliability

* [ ] Unit tests pass.
* [ ] Integration tests pass.
* [ ] End-to-end tests pass.
* [ ] Stress testing completed.
* [ ] No release-blocking bugs remain.

## Release

* [ ] Production build works.
* [ ] Clean installation works.
* [ ] User data location is correct.
* [ ] Application assets are included.
* [ ] README is updated.
* [ ] Supported platforms are documented.
* [ ] Build process is documented.

---

# 50. Final V2 Definition of Done

Comma V2 is considered complete when the following experience works reliably:

```text id="k7m2q9"
                    DESKTOP
┌────────────────────────────────────────────────────┐
│                                                    │
│                                                    │
│                                                    │
│                                      ┌─────────────┤
│                                      │ ●           │
│                                      ├─────────────┤
│                                      │ ●           │
│                                      ├─────────────┤
│                                      │ ●           │
└──────────────────────────────────────┴─────────────┘
```

The user:

```text id="w3p8n1"
sees a note at the edge
        ↓
hovers
        ↓
note reveals
        ↓
types
        ↓
leaves
        ↓
note collapses
        ↓
grabs it later
        ↓
moves it
        ↓
rearranges it
        ↓
archives it when finished
        ↓
exports it when needed
        ↓
restarts Comma
        ↓
everything is still there
```

The application should feel:

```text id="v9x4m2"
Fast
Quiet
Persistent
Predictable
Desktop-native
```

---

# 51. Final Release Gate

The V2 release may proceed only when:

```text id="q2m7x8"
All critical acceptance criteria
            +
All release-blocking bugs resolved
            +
Persistence verified
            +
End-to-end flow verified
            +
Clean installation verified
            +
Documentation updated
            +
Reference experience reviewed
            ↓
       COMMA V2 READY
```

---

# 52. Phase 9 Definition of Done

The final architectural result is:

> **Comma V2 is no longer an experiment or prototype. It is a self-contained, persistent desktop note application with a validated interaction model and a releasable build.**

At this point, the V2 roadmap is complete.

Any new functionality discovered afterward should enter a **V3 roadmap** rather than being quietly bolted onto V2.
