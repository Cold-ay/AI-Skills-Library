---
name: combination-react-motion
description: Build scoped, sequenced React animations with lifecycle cleanup.
---

# React motion studio

Build scoped, sequenced React animations with lifecycle cleanup.

Use only when this combination is explicitly requested. Follow the stages in order; do not load all skills at once. Host and user instructions take precedence. Never install dependencies, send data or run bundled scripts without reviewing them for the current task.

## Stages

### 1. Establish animation primitives

Read ../gsap-core/SKILL.md. Choose targets and tweens; document reduced-motion alternatives.

### 2. Compose the sequence

Read ../gsap-timeline/SKILL.md. Create named labels and intentional timing from the approved motion brief.

### 3. Integrate and verify cleanup

Read ../gsap-react/SKILL.md. Use scoped refs and useGSAP; check rerenders, unmount and reduced motion.

## Dependencies

React, gsap and @gsap/react. Runtime library terms are separate from skill MIT licenses.

## Conflicts and limits

Core examples do not override React lifecycle guidance. Use gsap-react cleanup in React. ScrollTrigger and other plugins are outside this pack.

Compatibility is proposed from static source review, not an end-to-end Codex runtime test. Stop and report missing dependencies rather than silently substituting tools.
