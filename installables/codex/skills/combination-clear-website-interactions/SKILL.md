---
name: combination-clear-website-interactions
description: Make controls discoverable, then specify honest feedback and recovery states.
---

# Clear website interactions

Make controls discoverable, then specify honest feedback and recovery states.

Use only when this combination is explicitly requested. Follow the stages in order; do not load all skills at once. Host and user instructions take precedence. Never install dependencies, send data or run bundled scripts without reviewing them for the current task.

## Stages

### 1. Clarify the action and outcome

Read ../design-everyday-things/SKILL.md. Audit one user journey; hand off a control map with labels, expected outcomes, constraints and recovery paths.

### 2. Specify and implement the state transitions

Read ../microinteractions/SKILL.md. Use the approved control map to define idle, focus, pending, success, failure and repeated-click behavior. Hand off a state matrix and keyboard/reduced-motion checks.

## Dependencies

A website or prototype with a specific task. Plain HTML/CSS/JavaScript works; no animation runtime or service is bundled. Review source before use; preserve existing project instructions.

## Conflicts and limits

Design of Everyday Things owns discoverability and task flow; Microinteractions owns local feedback within that flow. Optional sibling skills are not bundled. Numeric self-scores and user-study percentages are heuristics, not test results. Never show success before the real operation succeeds or infer that copying a command ran it.

Compatibility is proposed from static source review, not an end-to-end Codex runtime test. Stop and report missing dependencies rather than silently substituting tools.
