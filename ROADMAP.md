# Roadmap

This roadmap keeps the project honest about its current shape: a practical governance kit, not a full platform.

## v0.3: adoption quality

- Add more synthetic examples for multi-agent review, public export, and Obsidian-style notes.
- Provide one unified CLI entrypoint for the existing scripts.
- Add `doctor` checks for common setup mistakes.
- Add a handoff cleanup planner that inventories a messy handoff directory before humans or agents move files.
- Keep all examples synthetic and public-safe.

## v0.4: migration quality

- Add before/after migration examples.
- Add stronger validators for worker task briefs and review identity blocks.
- Add optional JSON schemas for machine-readable governance fragments.
- Add docs for adopting the kit in Hermes, Claude Code, Codex, and generic AGENTS.md workflows.

## v0.5: package quality

- Publish a tagged release with generated release notes.
- Harden command-line UX around `mpmg init`, `mpmg validate`, `mpmg audit`, `mpmg doctor`, and `mpmg worker-task`.
- Add cross-platform smoke tests for Windows, Linux, and macOS.

## Non-goals

- Storing project databases in this repo.
- Replacing secret scanners, compliance review, or domain-specific safety gates.
- Encoding private project histories, paths, targets, accounts, or run artifacts.
