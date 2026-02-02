# start.md – Agent Rules

This file is the fixed constitution for agent behavior in this repo.  
Do **not** edit it. Do **not** treat it as a task. Obey every rule below.

# Scope

- Only harvest data from external sources
- Save only to gitignored `data/` (jsonl/json/csv/parquet)
- No DB, no API, no scheduled jobs, no live-system changes

# Task Workflow – mandatory sequence

1. Write minimal task file in `agent-docs/tasks/[name].md`:
   - Goal
   - Source(s)
   - Core logic
   - Output path & format
   - Checklist  
     Show it to user → wait for explicit confirmation

2. Code only after user says go.

3. When you finish:
   - Review your checklist
   - Mark items done
   - Say exactly: “Task [name] ready for review”

4. **Never** run full harvesting, heavy requests, or long operations yourself. User runs and verifies everything.

5. Before starting any task: read `requirements.txt` + relevant existing files to match style/naming.

# Code & Structure Rules

- Every file must be **bite-sized** and have **one clear purpose**.  
  If it grows or mixes concerns → split immediately.

- Preferred layout:  
  `app/[name-of-project]/` (per-source)  
  `src/utils/` (shared helpers)

- Centralize:
  - HTTP client + retries + headers
  - File writing (atomic / append)
  - Rate limiting / delays

- When you create any major folder (`harvesters/`, `utils/`, etc.):  
  immediately add short `README.md` inside with:
  - Purpose
  - Main files
  - How to add new items

- have a sleep and polite headers in mind .
- do not over comment functions , but do comment what it does
- everything should have types so that it is easy to read and understand. use type heavily unless asked not to .
- Never inline: requests + parsing + saving in one function
- every function should do one thing and clear.
- main.py on each app would do the flow of scraping and creating the data file.
- Never mock data/responses during work
- Never create tests unless asked
- Never execute/simulate full runs
- every file is kebab-cased
- data/ outputs are per app, and default is csv.
