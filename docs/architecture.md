# Architecture

This project models memory governance as separate authority layers. The layers are intentionally redundant enough that a future agent can recover context, but not so redundant that stale facts spread across every memory store.

```mermaid
flowchart TD
    U[Current user / operator instruction] --> L[Live repo files + validation output]
    L --> H[Repo handoff: accepted changes, active queue, gates]
    H --> N[Project notes / Obsidian: strategy, rationale, reviews]
    N --> G[Global durable agent memory: compact signposts]
    G --> S[Session search: recall leads only]

    H --> W[External worker task]
    N --> W
    W --> R[Worker result / review artifact]
    R --> V[Coordinator verification]
    V --> H

    SK[Skills: reusable procedures] -. guide .-> V
    SK -. guide .-> W
```

## Layer contract

| Layer | Question it answers | Update cadence |
|---|---|---|
| Current instruction | What did the human ask now? | Each session/task |
| Live repo/files | What is actually true on disk? | Every verification |
| Repo handoff | What changed, what was verified, what is blocked? | After accepted work/reviews |
| Active queue | What is the current lane and next safe action? | After phase/priority changes |
| Project notes | Why are we doing this and what decisions matter long-term? | After durable strategy/rationale changes |
| Global memory | Where should future sessions look first? | Rare, compact updates |
| Skills | How should repeatable work be performed? | After reusable workflow lessons |

## Worker context boundary

External workers receive only what their wrapper/prompt includes plus what they choose to read from disk. A mature project therefore names required context reads in every worker task instead of assuming that global memory, chat history, or the full note vault is inherited.
