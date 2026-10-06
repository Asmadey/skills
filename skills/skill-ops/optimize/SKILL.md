
You are my token-efficiency engineer. Work in three phases and show your work.

PHASE 1 — AUDIT (read-only):

1. List everything preloaded into a fresh session — system tools, MCP servers
   (and how many tools each exposes), skills, CLAUDE.md — with token estimates.
   Is tool deferral ACTIVE or NOT? If a proxy, gateway, or router sits between
   me and the model, say so loudly.
2. Read my session logs (~/.claude/projects/**/*.jsonl, newest 10 sessions).
   Sum cache-read, cache-creation, input, and output tokens per turn.
   Report my "re-read waste %".
3. Measure every CLAUDE.md in scope — project, parent folders, user level,
   and @imports. Report each file's token size. Flag any file over 5k or
   totals over 10k, and anything over 200 lines.
4. List my skills with description lengths. Flag descriptions over 2 sentences.
5. Report current model and effort and where each is set. Flag any mode or
   agent config that switches models automatically mid-session (cache killer).
6. List scheduled/background tasks and their intervals. Flag any interval
   longer than 1 hour (cache expires, so every fire pays full price).
7. End Phase 1 with one table sorted by cost: FINDING | SEVERITY | EVIDENCE | COST.

PHASE 2 — FIX (apply, but show me each change before the next):

1. Create a PostToolUse hook that trims noisy command output (installs, builds,
   test runs) to the last 30 lines plus any error lines before it enters context.
2. Set a statusline showing model, context %, and session cost.
3. Add a guard block to CLAUDE.md: be concise; route mechanical work (rename,
   format, summarize, scrape) to a Haiku sub-agent; never suggest /compact as a
   cost-saving measure.
4. Trim CLAUDE.md to under 200 lines (archive removals to CLAUDE.archive.md).
5. Shorten bloated skill descriptions. List skills and MCP servers unused in my
   last 10 sessions as removal candidates — do not remove without asking.
6. For every scheduled task flagged in the audit: propose deleting it or
   retiming it to fire more often than the cache lifetime — apply only what
   I approve.

PHASE 3 — REPORT:
Show before/after: preload tokens, CLAUDE.md size, waste %. Then print my
5-habit card: /clear between jobs · pick model + effort once, never switch
mid-session · batch questions into one message · edit the message instead of
correcting · paste text, never PDFs or screenshots.
