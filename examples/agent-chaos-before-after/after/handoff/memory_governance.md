# Memory Governance

## Authority order

1. Current explicit operator instruction.
2. Live repo files and validation output.
3. Repo handoff files.
4. Project notes for long-term rationale.
5. Global durable memory as compact signposts only.
6. Session search as recall only.

## Global durable memory

Do not store project progress logs, run artifacts, private paths, or temporary decisions in global durable memory.

## External workers

External workers must receive explicit required reads, allowed files/scope, disallowed actions, expected output, and validation steps.
