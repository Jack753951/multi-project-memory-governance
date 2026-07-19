# Memory Governance

## Authority order by question

1. Task/scope: current explicit operator instruction.
2. Current observed state: direct observation of the relevant system of record and fresh question-matched evidence; repo files establish checkout state, while deployment/runtime claims require corresponding external evidence.
3. Intended behavior: current accepted requirements, specifications, and policies.
4. Accepted work state: verified repo handoff.
5. Long-term rationale: project notes.
6. Recall: compact global-memory signposts, then session search; verify changing facts.

## Global durable memory

Do not store project progress logs, run artifacts, private paths, or temporary decisions in global durable memory.

## External workers

External workers must receive explicit required reads, allowed files/scope, disallowed actions, expected output, and validation steps.
